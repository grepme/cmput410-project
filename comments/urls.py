from django.conf.urls import patterns, include, url

urlpatterns = patterns('comments.views',
                       (r'^new/$', 'new_comment'),
                       # (r'^delete/(?P<guid>[-\w]+)/$', 'delete_post'),
                       # (r'^all/', 'all_posts'),
                       # (r'^my/', 'my_posts')
)

#urlpatterns = patterns('posts.views', r'^delete/$', 'delete_post')
#url(r'^delete/(?P<id>\d+)/$','posts.views.delete_post')
#urlpatterns = patterns('posts.views',(r'^delete/(?P<id>\d+)/$', 'delete_post'),)