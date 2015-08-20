from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .slugify import slugify


class ValidateSlug(object):
    """
    Test whether the given value is an accepted slug.

    The class can test against custom slug functions (e.g. awesome-slugify).
    It should be used instead of the standard slug validators,
    because these only accept what the standard Django slugify() can process.
    """
    slugify = slugify
    message = _('Enter a valid slug.')
    code = 'invalid'

    def __init__(self, slugify=None, message=None, code=None):
        if slugify is not None:
            self.slugify = slugify
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        if self.slugify(value) != value:
            raise ValidationError(self.message, code=self.code)
