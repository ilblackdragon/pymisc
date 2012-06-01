# -*- coding: utf-8 -*-

import re
import string

from django.shortcuts import _get_queryset
from django.conf import settings
from django.http import HttpResponse
from django.utils.encoding import force_unicode, iri_to_uri

first_cyrillic_letter = unicode('а')
last_cyrillic_letter = unicode('я')

class HttpResponseReload(HttpResponse):
    """
    Reload page and stay on the same page from where request was made.

    example:

    def simple_view(request):
        if request.POST:
            form = CommentForm(request.POST):
            if form.is_valid():
                form.save()
                return HttpResponseReload(request)
        else:
            form = CommentForm()
        return render_to_response('some_template.html', {'form': form})
    """
    status_code = 302

    def __init__(self, request):
        HttpResponse.__init__(self)
        referer = request.META.get('HTTP_REFERER')
        self['Location'] = iri_to_uri(referer or "/")

def custom_spaceless(value):
    return re.sub('(\n|\r|(>))[ \t]+((?(2)<))', '\\1\\3', force_unicode(value))

def get_object_or_None(klass, *args, **kwargs):
    """
    Uses get() to return an object or None if the object does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), a MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None

def get_config(key, default):
    """
    Get settings from django.conf if exists,
    return default value otherwise

    example:

    ADMIN_EMAIL = get_config('ADMIN_EMAIL', 'default@email.com')
    """
    return getattr(settings, key, default)

def get_alphabets():
    alphabet_en = unicode(string.ascii_uppercase)
    alphabet_ru = []
    first = ord(first_cyrillic_letter)
    last = ord(last_cyrillic_letter)+1
    for ch in range(first, last):
        alphabet_ru.append(unichr(ch).upper()) 
    return (alphabet_en, alphabet_ru)
    
alphabet_en, alphabet_ru = get_alphabets()
