from django import template
import fsutil
from django.template.defaultfilters import stringfilter
from django.core.files.images import get_image_dimensions

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
    splitted = value.split('media_root')
    newvalue = '/media' + splitted[1]
    return newvalue


@register.filter
@stringfilter
def getimageHeight(value):
    height, width = get_image_dimensions(value)
    return height


@register.filter
@stringfilter
def getimageWidth(value):
    height, width = get_image_dimensions(value)
    return width
