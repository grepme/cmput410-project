from django.conf.urls import patterns, include, url

urlpatterns = patterns('friends.views',
                       (r'^$', 'friends'),
                       (r'search/(?P<name>([a-zA-Z0-9 -._~:?#%]+))/?$', 'search_friends'),
                       (r'all/?$', 'search_all'),
                       (r'sent/?$', 'sent_friends'),
                       (r'incoming/?$', 'incoming_friends'),
                       (r'following/?$', 'following_friends'),
                       (r'friends/?$', 'friends_friends'),
                       (r'delete/(?P<friend_guid>[-\w]+)/?$', 'delete'),
                       (r'^friendrequest$', 'friend_request'),
)
