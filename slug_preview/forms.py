from django import forms
from django.forms.forms import BoundField
from . import widgets
from .slugify import slugify, django_slugify
from .validators import ValidateSlug


class SlugPreviewFormMixin(object):
    """
    Form Mixin to add necessary integration for the SlugPreviewField.
    This extends the default ``form[field]`` interface that produces the BoundField for HTML templates.
    """
    def __getitem__(self, item):
        boundfield = super(SlugPreviewFormMixin, self).__getitem__(item)
        if isinstance(boundfield.field, SlugPreviewField):
            boundfield.__class__ = _upgrade_boundfield_class(boundfield.__class__)
        return boundfield


class BoundSlugField(BoundField):
    """
    An exta integration to pass information of the form to the widget.
    This is loaded via :class:`SlugPreviewFormMixin`
    """
    def as_widget(self, widget=None, attrs=None, only_initial=False):
        if not widget:
            widget = self.field.widget

        widget.instance = self.form.instance  # Widget needs ability to fill in the blanks.
        return super(BoundSlugField, self).as_widget(widget=widget, attrs=attrs, only_initial=only_initial)


UPGRADED_CLASSES = {}
def _upgrade_boundfield_class(cls):
    if cls is BoundField:
        return BoundSlugField
    elif issubclass(cls, BoundSlugField):
        return cls

    # When some other package also performs this same trick,
    # combine both classes on the fly. Avoid having to do that each time.
    # This is needed for django-parler
    try:
        return UPGRADED_CLASSES[cls]
    except KeyError:
        # Create once
        new_cls = type('BoundSlugField_{0}'.format(cls.__name__), (cls, BoundSlugField), {})
        UPGRADED_CLASSES[cls] = new_cls
        return new_cls


class SlugPreviewModelForm(SlugPreviewFormMixin, forms.ModelForm):
    """
    A default model form, configured with the :class:`SlugPreviewFormMixin`.
    """


class SlugPreviewField(forms.SlugField):
    """
    A Form field that displays the slug and preview.
    It requires the :class:`SlugPreviewFormMixin` to be present in the form.
    """
    widget = widgets.SlugPreviewWidget

    def __init__(self, *args, **kwargs):
        self.populate_from = kwargs.pop('populate_from', None)
        self.always_update = kwargs.pop('always_update', False)
        self.url_format = kwargs.pop('url_format', None)
        self.slugify = kwargs.pop('slugify', slugify)

        if self.slugify != django_slugify:
            # This replaces the 'default_validators' setting at object level.
            self.default_validators = [ValidateSlug(self.slugify)]

        super(SlugPreviewField, self).__init__(*args, **kwargs)
        self.widget.url_format = self.url_format

    def widget_attrs(self, widget):
        # Expose the form field settings to HTML
        attrs = super(SlugPreviewField, self).widget_attrs(widget)
        attrs.update({
            'data-populate-from': self.populate_from,
            'data-url-format': self.url_format,
            'data-always-update': self.always_update,
        })
        return attrs
