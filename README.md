# django-render-fields

**django-render-fields** is a Django app that enables flexible, declarative layout of model detail pages (or any model data display) inspired by the Django admin’s fieldsets. It allows you to define your page structure through simple Python `fieldsets` declarations and then render them cleanly in templates.

With **django-render-fields**, you gain full control over how model data is presented—making your detail pages easy to maintain, consistent, and visually organized without repeating boilerplate code.

## Features

The app provides two useful template tags to help you customize your views:

- **`render_fieldsets`**: Parses a Django admin-style `fieldsets` object and renders the grouped fields accordingly. Useful for uncomplicated layouts that follow simple fieldset structures.
- **`render_field`**: Renders a single model field with label, value, and optional formatting. Useful for complicated layouts that require rendering fields individually or in a custom order.

Additionally, a view mixin class is provided that lets you declare either fields or fieldsets (just like Django admin), simplifying the setup of detail views with configurable layouts.

## Installation

1. Install the package using pip:

   ```bash
   pip install django-render-fields
   ```
2. Add `render_fields` to your `INSTALLED_APPS` in your Django settings:

   ```python
    INSTALLED_APPS = [
         ...
         'render_fields',
    ]
    ```

## Usage

The `FieldsetsMixin` provides an easy way to declaratively define the layout of your model detail views by specifying either `fields` or `fieldsets`, similar to how Django admin handles form layouts.

    from django.views.generic import DetailView
    from django_render_fields.views import FieldsetsMixin
    from .models import MyModel

    class MyModelDetailView(FieldsetsMixin, DetailView):
        model = MyModel

        # Option 1: Define a simple list of fields to display in order
        fields = ['field1', ('field2', 'field3')]

        # Option 2: Define fieldsets to group fields and optionally add titles and descriptions
        fieldsets = (
            ('Main Info', {
                'fields': ['field1', ('field2', 'field3')],
                'description': 'Basic information about the object.'
            }),
            ('Additional Details', {
                'fields': (('field4', 'field5'),),  # tuple inside tuple for row layout
            }),
        )

Note: For more complex situations, you can override the `get_fieldsets` method to customize the fieldset generation logic.

### How it works

- If `fields` is defined, it will render all fields in a fieldset with no label.
- If `fieldsets` is defined, it expects a Django admin-style iterable of `(title, options)` tuples, where `options` is a dictionary with:

    - `'fields'`: A list or tuple of field names. Nested tuples/lists will render fields side-by-side in a row.
    - Optional `'description'`: A string description to display under the fieldset title.

### In your template

If you are using the `FieldsetsMixin`, a `fieldsets` context variable will be injected into your template. You can use this variable to render the fieldsets using the `render_fieldsets` template tag:

    {% load render_fields %} 
    <div class="model-detail"> 
        {% render_fieldsets object fieldsets %}
    </div>

### Rendering individual fields

For fine-grained control over how individual fields are rendered, you can use the `render_field` template tag. This is useful when you want a consistent look and feel to how data are rendered but you need exact control over the layout.

    {% load render_fields %}
    <div class="model-detail">
        {% render_field object "field1" %}
        {% render_field object "field2" %}
        {% render_field object "field3" %}
    </div>

## Customization


### Customizing layout

**django-render-fields** is designed to be flexible and easily customizable. You can change the layout and appearance of your rendered model detail pages by overriding the default templates it provides.

The layout is controlled by two main templates: `fieldsets/fieldset.html` and `fieldsets/row.html`. These templates define how fieldsets and rows of fields are rendered, respectively.

#### `fieldsets/fieldset.html`

This template receives the `fieldsets` context variable and is responsible for rendering the entire fieldset structure. It is called by the `render_fieldsets` template tag.

    {% load render_fieldsets %}

    {% for title, fieldset in fieldsets %}
    <fieldset>
        {% if title %}
            <legend>{{ title }}</legend>
        {% endif %}
        {% if fieldset.description %}
            <p>{{ fieldset.description }}</p>
        {% endif %}
        {% for row in fieldset.fields %}
            {% render_row object row %}
        {% endfor %}
    </fieldset>
    {% endfor %}

#### `fieldsets/row.html`

This template controls how a single row of fields is rendered. The default looks like this:

    {% load render_fieldsets %}

    <div class="row">
    {% for field in fields %}
        <div class="col-md">
        {% render_field object field %}
        </div>
    {% endfor %}
    </div>

### Customizing all fields

The `fieldsets/wrapper.html` template provides a wrapper around **all individual fields**. To customize how fields appear globally, override this template.

    <div class="mb-3">
        <div class="fw-semibold">
            <span>{{ label }}</span>
        </div>
        <div>{% include field_template %}</div>
    </div>

It receives the following context variables:

| Variable | Description |
| --- | --- |
| `field` | The model field object being rendered (e.g. self._meta.get_field("field1")) |
| `label` | Label text for the field |
| `help_text` | Help text associated with the field (if any) |
| `value` | Value of the field extracted from the object |
| `choice_label` | Label for choice fields (if applicable) |
| `field_template` | The actual template rendering the field value |
| `missing` | Placeholder text for missing/empty values |

### Customizing individual fields

The `field_template` variable in the `wrapper.html` template will be a list of possible templates used to render the field. At the moment, the list looks like this:

```python
    templates = [
        f"fieldsets/fields/{field.__class__.__name__.lower()}",
        "fieldsets/fields/default.html",
        ]
```

The `default.html` template is a fallback for when a specific field type does not have a dedicated template. This template is suitable for most simple field types and can be customized to fit your needs.

To customize rendering of specific field types (especially useful for more complex field types), you can create custom templates by adding a new template file in the `fieldsets/fields/` directory. 

Each field template will receive the same context variables as `wrapper.html`, allowing you to customize how each field type is displayed.

Example template for a `ForeignKey` field:

```html
<!-- fieldsets/fields/foreignkey.html -->
<div class="wrapper-element">
    {% for related in value.all %}
        <a href="{{ related.get_absolute_url }}">{{ related }}</a>
    {% endfor %}
</div>
```
