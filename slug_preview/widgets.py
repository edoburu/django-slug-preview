from __future__ import unicode_literals
import re

from django.conf import settings
from django.forms import widgets
from django.utils.html import format_html


class SlugPreviewWidget(widgets.TextInput):
    """
    Slug preview
    """
    class Media:
        css={
            'all': (
                'slug_preview/css/slug_preview.css',
            )
        }
        js=(
            'admin/js/vendor/jquery/jquery{}.js'.format('' if settings.DEBUG else '.min'),
            'admin/js/jquery.init.js',
            'admin/js/urlify.js',
            'admin/js/prepopulate{}.js'.format('' if settings.DEBUG else '.min'),
            'slug_preview/js/slug_preview.js',
        )

    def __init__(self, attrs=None, url_format=None):
        super(SlugPreviewWidget, self).__init__(attrs=attrs)
        self.url_format = url_format
        self.instance = None   # assigned via BoundSlugField

    def render(self, name, value, attrs=None, **kwargs):
        if attrs is None:
            attrs = {}
        input_tag = super(SlugPreviewWidget, self).render(name, value, attrs=attrs, **kwargs)
        return format_html('<kbd class="slugpreview">{0}</kbd>', self.render_preview(input_tag))

    def render_preview(self, input_tag):
        url_format = self.url_format
        if not url_format:
            # Late evaluation, to allow access to self.instance
            if self.instance is not None and hasattr(self.instance, 'get_absolute_url_format'):
                url_format = self.instance.get_absolute_url_format()
            else:
                url_format = u'/{slug}/'

        before, after = url_format.split('{slug}', 2)
        return format_html(
            '<span class="url-prefix">{before}</span>'     # noqa indent
            '<span class="url-slug">{input_tag}</span>'
            '<span class="url-suffix">{after}</span>',
            before=before,
            input_tag=input_tag,
            after=after,
        )
