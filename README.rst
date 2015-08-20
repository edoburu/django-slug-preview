django-slug-preview
===================

An advanced slug field offering live URL previews.

This is inspired by the "Permalink" preview that WordPress offers.
While not looking as fancy yet, this is a good start for Django projects.
Improvements are welcome!


.. figure:: https://github.com/edoburu/django-slug-preview/raw/master/docs/images/slugpreview1.png
   :width: 632px
   :height: 95px


Installation
============

First install the module, preferably in a virtual environment.
It can be installed from PyPI::

    pip install django-slug-preview

Or the current folder can be installed for development::

    pip install -e .

Add ``slug_preview`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS += (
        'slug_preview',
    )


Usage
=====

* Use ``slug_preview.models.SlugPreviewField`` in your models instead of the standard ``models.SlugField``.
* Add ``slug_preview.forms.SlugPreviewFormMixin`` in your forms.

For example::

    from django.db import models
    from slug_preview.models import SlugPreviewField

    class MyModel(models.Model):
        slug = SlugPreviewField(_("Slug"))


In the admin you can use the ``SlugPreviewModelForm`` shortcut::

    from django.contrib import admin
    from django import forms
    from slug_preview.forms import SlugPreviewModelForm

    @admin.register(MyModel)
    class MyModelAdmin(admin.ModelAdmin):
        form = SlugPreviewModelForm


In custom forms, use ``SlugPreviewFormMixin`` directly::

    from django import forms
    from slug_preview.forms import SlugPreviewFormMixin
    from .models import MyModel

    class MyModelForm(SlugPreviewFormMixin, forms.ModelForm):
        class Meta:
            model = MyModel


Special model URLS
~~~~~~~~~~~~~~~~~~

When a model has a custom URL layout (not just ``/{slug}/``), you can add a ``get_absolute_url_format()`` method in the model.
For example::

    from django.db import models
    from slug_preview.models import SlugPreviewField

    class Page(models.Model):
        parent = models.ForeignKey('self')
        slug = SlugPreviewField(_("Slug"))
        # ...


        def get_absolute_url(self):
            if self.parent_id:
                return "{0}{1}/".format(self.parent.get_absolute_url(), self.slug)
            else:
                return "/{0}/".format(self.slug)

        def get_absolute_url_format(self):
            if self.parent_id:
                return "{0}{{slug}}/".format(self.parent.get_absolute_url())
            else:
                return "/{slug}/"

For a blog, you can add the ``/blog/{year}/{month}/`` format too::

    from django.core.urlresolvers import reverse
    from django.db import models
    from django.utils.timezone import now
    from slug_preview.models import SlugPreviewField

    class Article(models.Model):
        slug = SlugPreviewField(_("Slug"))
        pubdate = models.DateTimeField(default=now)
        # ...


        def get_absolute_url(self):
            root = reverse('article_list')
            return "{root}/{year}/{month}/{slug}/".format(
                root=reverse('article_list').rstrip('/'),
                year=self.pubdate..strftime('%Y'),
                monthy=self.pubdate..strftime('%M'),
                slug=self.slug
            )

        def get_absolute_url_format(self):
            root = reverse('article_list')
            pubdate = self.pubdate or now()
            return "{root}/{year}/{month}/{{slug}}/".format(
                root=reverse('article_list').rstrip('/'),
                year=pubdate.strftime('%Y'),
                monthy=pubdate.strftime('%M'),
            )


Improving this package
======================

This module is designed to be usable for other projects too.
In case there is anything you didn't like about it,
or think it's not flexible enough, please let us know.
We'd love to improve it! Pull requests are welcome too. :-)
