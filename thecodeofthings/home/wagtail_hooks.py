from wagtail.admin.rich_text.converters import html_to_contentstate
from wagtail.admin.rich_text.editors.draftail import features as draftail_features
from wagtail.core import hooks


@hooks.register("register_rich_text_features")
def register_cite_feature(features):
    """
    Registering the `cite` feature, which uses the `CITE` Draft.js inline style type,
    and is stored as HTML with a `<cite>` tag.
    """
    feature_name = "cite"
    type_ = "CITE"
    tag = "cite"

    # Configure how Draftail handles the feature in its toolbar.
    control = {
        "type": type_,
        "label": "cite",
        "description": "Cite",
        "style": {"fontStyle": "italic"},
    }

    # Call register_editor_plugin to register the configuration for Draftail.
    features.register_editor_plugin("draftail", feature_name, draftail_features.InlineStyleFeature(control))

    # Configure the content transform from the DB to the editor and back.
    db_conversion = {
        "from_database_format": {tag: html_to_contentstate.InlineStyleElementHandler(type_)},
        "to_database_format": {"style_map": {type_: tag}},
    }

    # Call register_converter_rule to register the content transformation conversion.
    features.register_converter_rule("contentstate", feature_name, db_conversion)

    # Add the feature to the default features list to make it available
    # on rich text fields that do not specify an explicit "features" list
    features.default_features.append("cite")


@hooks.register("register_rich_text_features")
def register_em_feature(features):
    """
    Registering the `em` feature, which uses the `EM` Draft.js inline style type,
    and is stored as HTML with a `<em>` tag.
    """
    feature_name = "em"
    type_ = "EM"
    tag = "em"

    # Configure how Draftail handles the feature in its toolbar.
    control = {
        "type": type_,
        "label": "em",
        "description": "emphasis",
        "style": {"fontStyle": "italic"},
    }

    # Call register_editor_plugin to register the configuration for Draftail.
    features.register_editor_plugin("draftail", feature_name, draftail_features.InlineStyleFeature(control))

    # Configure the content transform from the DB to the editor and back.
    db_conversion = {
        "from_database_format": {tag: html_to_contentstate.InlineStyleElementHandler(type_)},
        "to_database_format": {"style_map": {type_: tag}},
    }

    # Call register_converter_rule to register the content transformation conversion.
    features.register_converter_rule("contentstate", feature_name, db_conversion)

    # Add the feature to the default features list to make it available
    # on rich text fields that do not specify an explicit "features" list
    features.default_features.append("em")


@hooks.register("register_rich_text_features")
def register_cite_essay_feature(features):
    """
    Registering the `cite-essay` feature, which uses the `cite-essay` Draft.js inline style type,
    and is stored as HTML with a `<cite class="essay">` tag.
    """
    feature_name = "cite-essay"
    type_ = "cite-essay"

    # Configure how Draftail handles the feature in its toolbar.
    control = {
        "type": type_,
        "label": "essay",
        "description": "Cite as essay",
        "style": {"fontStyle": "italic", "textDecoration": "underline dotted"},
        "element": "cite",
    }

    # Call register_editor_plugin to register the configuration for Draftail.
    features.register_editor_plugin("draftail", feature_name, draftail_features.InlineStyleFeature(control))

    # Configure the content transform from the DB to the editor and back.
    db_conversion = {
        "from_database_format": {"cite[class=essay]": html_to_contentstate.InlineStyleElementHandler(type_)},
        "to_database_format": {"style_map": {type_: {"element": "cite", "props": {"class": "essay"}}}},
    }

    # Call register_converter_rule to register the content transformation conversion.
    features.register_converter_rule("contentstate", feature_name, db_conversion)

    # Add the feature to the default features list to make it available
    # on rich text fields that do not specify an explicit "features" list
    features.default_features.append("cite-essay")


@hooks.register("register_rich_text_features")
def register_aside_essay_feature(features):
    """
    Registering the `aside` feature, which uses the `ASIDE` Draft.js block type,
    and is stored as HTML with a `<aside class="marginalia">` tag.
    """
    feature_name = "aside"
    type_ = "ASIDE"

    # Configure how Draftail handles the feature in its toolbar.
    control = {
        "type": type_,
        "label": "aside",
        "description": "Marginalia",
        "element": "aside",
    }

    # Call register_editor_plugin to register the configuration for Draftail.
    features.register_editor_plugin(
        "draftail",
        feature_name,
        draftail_features.BlockFeature(control, css={"all": ["admin/css/aside.css"]}),
    )

    # Configure the content transform from the DB to the editor and back.
    db_conversion = {
        "from_database_format": {"aside[class=marginalia]": html_to_contentstate.BlockElementHandler(type_)},
        "to_database_format": {"block_map": {type_: {"element": "aside", "props": {"class": "marginalia"}}}},
    }

    # Call register_converter_rule to register the content transformation conversion.
    features.register_converter_rule("contentstate", feature_name, db_conversion)

    # Add the feature to the default features list to make it available
    # on rich text fields that do not specify an explicit "features" list
    features.default_features.append("aside")
