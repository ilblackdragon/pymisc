# -*- coding: utf-8 -*-

import urllib

from django.template import Library
from django.utils.translation import get_language_from_request, ugettext
from django.contrib.sites.models import Site
from django.conf import settings

register = Library()

def current_site_url():
    """Returns fully qualified URL (no trailing slash) for the current site."""
    protocol = getattr(settings, 'MY_SITE_PROTOCOL', 'http')
    port     = getattr(settings, 'MY_SITE_PORT', '')
    url = '%s://%s' % (protocol, settings.SITE_DOMAIN)
    if port:
        url += ':%s' % port
    return url

@register.simple_tag
def tweet_it(url, title):
    return """
        <div class="twitter">
            <a href="http://twitter.com/home/?%s" title="%s" target="_blank"></a>
        </div>    
    """ % (urllib.urlencode({'status': title + (unicode(" ") + url + unicode(" #escalibro")).encode('utf-8')}), ugettext("Tweet it"))    
    
@register.simple_tag
def buzz_it(url, title):
    return """
        <div class="buzz">
            <a onclick="window.open(this.href, '%s', 'width=800,height=300'); return false" href="http://www.google.com/buzz/post?%s" title="%s" target="_blank"></a>
        </div>    
    """ % (ugettext("Post link on Buzz"), urllib.urlencode({'url': url, 'message': title}), ugettext("Buzz it"))
    
@register.simple_tag
def facebook_it(url, title):
    return """
        <div class="facebook">
            <a onclick="window.open(this.href, '%s', 'width=800,height=300'); return false" href="http://www.facebook.com/sharer.php?%s" title="%s" target="_blank"></a>
        </div>
    """ % (ugettext("Share link on FaceBook"), urllib.urlencode({'u': url, 't': title}), ugettext("To FaceBook"))

@register.simple_tag
def vk_it(url, title):
    return """
        <div class="vk">
            <a onclick="window.open(this.href, '%s', 'width=800,height=300'); return false" href="http://vkontakte.ru/share.php?%s" title="%s"></a>
        </div>
    """ % (ugettext("Share link on VKontakte"), urllib.urlencode({'url': url, 'title': title}), ugettext("To VKontakte"))

    
functions = [tweet_it, buzz_it, facebook_it, vk_it] # Ordering
    
@register.simple_tag
def share_it(url, title):
    url = current_site_url() + url
    title = title.encode('utf-8')
    res = "<div class=\"share_buttons\">"
    for f in functions:
        res += f(url, title)
    res += "</div>"
    return res
