from django.conf.urls import patterns, include, url

urlpatterns = patterns('user_profile.views',
                       (r'^$', 'user_profile'),
                       (r'^/$', 'login'),
                       (r'^dashboard/$', 'dashboard'),
                       (r'^logout/$', 'logout'),
)