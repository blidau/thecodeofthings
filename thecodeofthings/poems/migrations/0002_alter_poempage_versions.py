# Generated by Django 3.2.11 on 2022-01-25 07:16

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("poems", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="poempage",
            name="versions",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "version",
                        wagtail.core.blocks.StructBlock(
                            [
                                ("title", wagtail.core.blocks.CharBlock()),
                                ("description", wagtail.core.blocks.RichTextBlock(required=False)),
                                ("featured_image", wagtail.images.blocks.ImageChooserBlock(required=False)),
                                ("date_created", wagtail.core.blocks.DateTimeBlock()),
                                ("date_released", wagtail.core.blocks.DateTimeBlock(required=False)),
                                ("date_modified", wagtail.core.blocks.DateTimeBlock(required=False)),
                                ("link", wagtail.core.blocks.URLBlock(required=False)),
                            ]
                        ),
                    )
                ],
                blank=True,
            ),
        ),
    ]
