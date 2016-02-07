from django.conf import settings
from django.db import models
from django.utils.encoding import force_text
from . import forms
from .slugify import slugify, django_slugify
from .validators import ValidateSlug


class SlugPreviewField(models.SlugField):
    """
    Slug field that also displays a preview.
    """
    def __init__(self, *args, **kwargs):
        self.populate_from = kwargs.pop('populate_from', None)  # nice idea from django-autoslug, but used differently.
        self.always_update = kwargs.pop('always_update', False)
        self.slugify = kwargs.pop('slugify', slugify)
        self.url_format = kwargs.pop('url_format', None)

        if self.slugify != django_slugify:
            # This replaces the 'default_validators' setting at object level.
            self.default_validators = [ValidateSlug(self.slugify)]

        super(SlugPreviewField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        # Pass our custom settings to the form field
        defaults = {
            'form_class': forms.SlugPreviewField,
            'populate_from': self.populate_from,
            'always_update': self.always_update,
            'slugify': self.slugify,
            'url_format': self.url_format,
        }
        defaults.update(kwargs)
        return super(SlugPreviewField, self).formfield(**defaults)

    def pre_save(self, instance, add):
        """
        Auto-generate the slug if needed.
        """
        # get currently entered slug
        value = self.value_from_object(instance)
        slug = None

        # auto populate (if the form didn't do that already).
        # If you want unique_with logic, use django-autoslug instead.
        # This model field only allows parameters which can be passed to the form widget too.
        if self.populate_from and (self.always_update or not value):
            value = getattr(instance, self.populate_from)

        # Make sure the slugify logic is applied,
        # even on manually entered input.
        if value:
            value = force_text(value)
            slug = self.slugify(value)
            if self.max_length < len(slug):
                slug = slug[:self.max_length]

        # make the updated slug available as instance attribute
        setattr(instance, self.name, slug)
        return slug

    def south_field_triple(self):
        from south.modelsinspector import introspector
        path = "{0}.{1}".format(self.__class__.__module__, self.__class__.__name__)
        args, kwargs = introspector(self)
        return (path, args, kwargs)


# Avoid using AdminTextInputWidget
if 'django.contrib.admin' in settings.INSTALLED_APPS:
    from django.contrib.admin import options
    options.FORMFIELD_FOR_DBFIELD_DEFAULTS[SlugPreviewField] = {}
