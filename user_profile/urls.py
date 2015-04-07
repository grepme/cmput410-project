from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from api.urls import id_regex

print '^({})/$'.format(id_regex)

urlpatterns = patterns('user_profile.views',
                       (r'^$', 'user_profile'),
                       (r'^update/$', 'update_profile'),
                       (r'(?P<guid>{})$'.format(id_regex), 'profile'),
                       (r'^update/pic/$', 'update_profilepic')
)
