from django import template
import fsutil
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def foldername(value):
    try:
        name = fsutil.split_path(value)[-1]
    except Exception as e:
        name = ''
    return name


@register.filter
@stringfilter
def filename(value):
    try:
        basename, extension = fsutil.split_filename(value)
        name = basename + '.' + extension
    except Exception as e:
        name = ''
    return name


@register.filter
def is_image(value):
    name = filename(value)
    if name.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        return True
    else:
        return False


@register.filter
@stringfilter
def urlfile(value):
    name = filename(value)
    if name.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        splitted = value.split('media_root')
        newvalue = '/media' + splitted[1]
    else:
        newvalue = value
    return newvalue
