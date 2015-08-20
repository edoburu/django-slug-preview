from __future__ import absolute_import
from django.utils.text import slugify as django_slugify

try:
    # awesome-slugify, unicode-slugify
    from slugify import slugify
except ImportError:
    # Fallback to Django ASCII-only support
    slugify = django_slugify
