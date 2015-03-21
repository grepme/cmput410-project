from django.conf.urls import patterns, include, url

urlpatterns = patterns('friends.views',
                       (r'^$', 'friends'),
                       (r'^search/?$', 'search_friends')
)
