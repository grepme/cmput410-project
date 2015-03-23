from django.conf.urls import patterns, include, url

urlpatterns = patterns('friends.views',
                       (r'^$', 'friends'),
                       (r'search/(?P<name>([a-zA-Z0-9 -._~:?#%]+))/?$', 'search_friends'),
                       (r'sent/?$', 'sent_friends'),
)
