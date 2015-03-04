from django.conf.urls import patterns, include, url

urlpatterns = patterns('user_profile.views',
                       (r'^$', 'user_profile'),
                       (r'^(?P<author>)/$', 'profile')
)