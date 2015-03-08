from django.conf.urls import patterns, include, url

urlpatterns = patterns('posts.views',
                       (r'^new/$', 'new_post'),
)