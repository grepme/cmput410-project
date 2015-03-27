from django.conf.urls import patterns, include, url

urlpatterns = patterns('comments.views',
                       (r'^new/$', 'new_comment'),
)
