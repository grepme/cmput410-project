from django.conf.urls import patterns, include, url

urlpatterns = patterns('friends.views',
                       (r'^$', 'friends'),
                       (r'search/(?P<name>([a-zA-Z0-9 -._~:?#%]+))/?$', 'search_friends'),
                       (r'sent/?$', 'sent_friends'),
                       (r'incoming/?$', 'incoming_friends'),
                       (r'following/?$', 'following_friends'),
                       (r'friends/?$', 'friends_friends'),
                       (r'remove/(?P<display_name>([a-zA-Z0-9 -._~:?#%]+))/?$', 'remove_friend'),
)
