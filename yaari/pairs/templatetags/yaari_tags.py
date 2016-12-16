
import os

from django.conf import settings
from django import template

register = template.Library()


@register.simple_tag
def staticfile(path):
    # Dev - just serve it normally
    if settings.DEBUG:
        return settings.STATIC_URL + path
    # Prod - append mtime to version the static files
    file_path = os.path.join(settings.STATIC_ROOT, path)
    url = '%s%s?v=%s' % (settings.STATIC_URL, path,
                         os.stat(file_path)[stat.ST_MTIME] if os.path.isfile(file_path) else '')
    return url
