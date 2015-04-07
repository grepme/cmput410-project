from django.conf.urls import patterns, include, url

guid_regex = "[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
sha1_regex = "[a-zA-Z0-9]+"
id_regex = "(({guid})|({sha1}))".format(guid=guid_regex,sha1=sha1_regex)


urlpatterns = patterns('api.views',

                        # get posts by a specific author that the current authenticated user
                        # can view
#                       author/id1/posts
                        #  /api/author/ef3e0e05-c5f8-11e4-a972-b8f6b116b2b7/posts/
                        (r'^author/(?:(?P<author_id>{})/?)?posts/?(?:/(?P<page>\d*)/?)?$'.format(id_regex), 'get_posts'),

                       # Get a specific post or all public posts
                       (r'^posts/?(?:(?P<post_id>{}))?/?$'.format(id_regex), 'get_post'),

                       #See if a author_id is a friend with author_2_id
                       (r'^friends/(?P<author_id>{0})/(?P<author_2_id>{0})/?$'.format(id_regex), 'is_friend'),

                       # POST authors, returns list of friends in the list
                       (r'^friends/(?P<author_id>{})/?$'.format(id_regex), 'get_friends'),

                       # GET authors on our server
                       (r'^author$', 'get_authors'),

                       # GET author on our server
                       (r'^author/(?P<profile_id>{})/?$'.format(id_regex), 'get_author'),

                       # Make a friend request with another user
                       (r'^friendrequest$', 'friend_request'),

                       # Follow a specific user
                       (r'^follow$', 'follow_user'),

                        # search for a user
                       #(r'search/(?P<name>([a-zA-Z0-9 -._~:?#%]+))/?$', 'search_users'),
)
