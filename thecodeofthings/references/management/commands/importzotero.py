from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import text, timezone
from pyzotero import zotero

from blog import models as blog_models
from references import models as reference_models


class Command(BaseCommand):
    help = "Import Zotero references"

    def handle(self, *args, **options):
        zot = zotero.Zotero(settings.ZOTERO_USER_ID, "user", settings.ZOTERO_API_KEY)
        zotero_collections = zot.collections()

        zotero_references = set()
        for zotero_collection in zotero_collections:
            zotero_collection_key = zotero_collection["data"]["key"]
            zotero_collection_name = zotero_collection["data"]["name"]
            self.stdout.write(f"Checking collection: {zotero_collection_name}")
            try:
                category = blog_models.Category.objects.get(name=zotero_collection_name)
                self.stdout.write(f"Getting category: {category.name}")
                collection, collection_created = reference_models.Collection.objects.update_or_create(
                    key=zotero_collection_key,
                    defaults={
                        "category": category,
                        "name": zotero_collection_name,
                    },
                )
                self.stdout.write(
                    f"{'Created' if collection_created else 'Updated'}"
                    f" collection: {zotero_collection_name} ({zotero_collection_key})"
                )
            except blog_models.Category.DoesNotExist:
                self.stdout.write(f"Skipping collection '{zotero_collection_name}' as no category exists")
                continue
            zotero_collection_references = set()
            collection_items = zot.everything(zot.collection_items(zotero_collection_key))
            self.stdout.write(f"Number of results: {len(collection_items)}")

            for collection_item_container in collection_items:
                collection_item = collection_item_container["data"]
                if collection_item["itemType"] not in reference_models.ReferenceType.values:
                    continue

                # Get the key
                key = collection_item.pop("key")
                zotero_references.add(key)
                zotero_collection_references.add(key)

                # Delete collection key as each collection is iterated through
                collection_item.pop("collections", None)

                # Delete other unused keys
                collection_item.pop("relations", None)
                collection_item.pop("tags", None)
                collection_item.pop("accessDate", None)

                # Emails has a subject and don't use title
                title = collection_item.pop("title", "")
                subject = collection_item.pop("subject", "")

                zotero_creators = collection_item.pop("creators", [])
                defaults = {
                    "item_type": collection_item.pop("itemType"),
                    "version": collection_item.pop("version", None),
                    "title": title if title else subject,
                    "short_title": collection_item.pop("shortTitle", ""),
                    "abstract_note": collection_item.pop("abstractNote", ""),
                    "date": collection_item.pop("date", ""),
                    "url": collection_item.pop("url", ""),
                    "language": collection_item.pop("language", ""),
                    "rights": collection_item.pop("rights", ""),
                    "extra": collection_item.pop("extra", ""),
                    "date_added": timezone.make_aware(
                        datetime.strptime(collection_item.pop("dateAdded"), "%Y-%m-%dT%H:%M:%SZ")
                    ),
                    "date_modified": timezone.make_aware(
                        datetime.strptime(collection_item.pop("dateModified"), "%Y-%m-%dT%H:%M:%SZ")
                    ),
                }
                # Add additional fields
                defaults["additional"] = collection_item
                # Get or create the key
                reference, reference_created = reference_models.Reference.objects.get_or_create(
                    key=key, defaults=defaults
                )

                if (not reference_created) and (reference.date_modified < defaults["date_modified"]):
                    self.stdout.write(f"Reference {defaults['title']} ({key}) updated due to change")
                    for key, value in defaults.items():
                        setattr(reference, key, value)
                    reference.save()
                elif not reference_created:
                    self.stdout.write(f"Reference {defaults['title']} ({key}) already exists")
                elif reference_created:
                    self.stdout.write(f"Reference {defaults['title']} ({key}) created")

                reference_roles = []
                for zotero_creator in zotero_creators:
                    try:
                        creator, creator_created = reference_models.Creator.objects.get_or_create(
                            first_name=zotero_creator["firstName"], last_name=zotero_creator["lastName"]
                        )
                    except KeyError:
                        creator, creator_created = reference_models.Creator.objects.get_or_create(
                            first_name=zotero_creator["name"],
                        )
                    if creator_created:
                        self.stdout.write(f"Creator {creator.get_full_name()} created")
                        creator.slug = text.slugify(creator.get_full_name())
                        creator.save()
                    role, _ = reference_models.Role.objects.get_or_create(
                        reference=reference, creator=creator, title=zotero_creator["creatorType"]
                    )
                    reference_roles.append(role.pk)
                # Remove unassociated creator roles
                unassociated_roles = reference_models.Role.objects.filter(reference=reference).exclude(
                    pk__in=reference_roles
                )
                for unassociated_role in unassociated_roles:
                    unassociated_role.delete()
                    self.stdout.write(
                        f"Removed {unassociated_role.title} '{unassociated_role.creator.get_full_name()}'"
                        f" from reference {reference.title}"
                    )
                reference.collections.add(collection)
            # Remove unassociated references
            removed_references = reference_models.Reference.objects.filter(collections=collection).exclude(
                key__in=zotero_collection_references
            )
            for removed_reference in removed_references:
                self.stdout.write(
                    f"Removed '{removed_reference.title}' ({removed_reference.key})"
                    f" from collection {collection.name}"
                )
                removed_reference.collections.remove(collection)
        # Delete references with no collections
        deletion_references = reference_models.Reference.objects.exclude(key__in=zotero_references)
        for deleted_reference in deletion_references:
            deleted_reference.delete()
            self.stdout.write(f"Deleted reference '{deleted_reference.title}' ({deleted_reference.key})")
        # Delete orphan creators
        orphan_creators = reference_models.Creator.objects.filter(role__isnull=True)
        for orphan_creator in orphan_creators:
            orphan_creator.delete()
            self.stdout.write(f"Removed orphan creator {orphan_creator.get_full_name()}")
        self.stdout.write("Import completed")
