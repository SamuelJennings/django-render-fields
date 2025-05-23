from django import template
from django.core.exceptions import FieldDoesNotExist

# import flatattrs
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag
def render_field(obj, fname):
    """Takes an object and a single field and renders it using the correct template based on the field type."""

    templates = ["render_fields/fields/default.html"]

    try:
        field = obj._meta.get_field(fname)
        field_type = field.__class__.__name__.lower()
        templates = [f"render_fields/fields/{field_type}.html", *templates]
    except FieldDoesNotExist:
        field = None

    value = getattr(obj, fname)

    choice_label = None
    if field and getattr(field, "choices", None):
        choice_label = dict(field.choices).get(value)

    if field and hasattr(field, "verbose_name"):
        label = getattr(field, "verbose_name", None)
        help_text = getattr(field, "help_text", None)
    else:
        help_text = None
        label = field.related_model._meta.verbose_name_plural

    return render_to_string(
        "render_fields/wrapper.html",
        {
            "field": field,
            "label": label,
            "help_text": help_text,
            "value": value,
            "choice_label": choice_label,
            "field_template": templates,
            "missing": "–",
        },
    )


@register.inclusion_tag("render_fields/fieldset.html")
def render_fieldsets(obj, fieldsets):
    """Renders a list of fieldsets for the given object."""
    if isinstance(fieldsets, dict):
        fieldsets = fieldsets.items()
    return {
        "object": obj,
        "fieldsets": fieldsets,
    }


@register.inclusion_tag("render_fields/row.html")
def render_row(obj, row):
    if isinstance(row, str):
        row = [row]
    return {
        "fields": row,
        "object": obj,
    }
