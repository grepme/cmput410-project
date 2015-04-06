from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('user_profile.views',
                       (r'^$', 'user_profile'),
                       (r'^update/$', 'update_profile'),
                       (r'^(\w+)/$', 'profile'),
                       (r'^update/pic/$', 'update_profilepic')
) 