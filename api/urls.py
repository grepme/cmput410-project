from django.conf.urls import patterns, include, url


urlpatterns = patterns('api.views',

                        # get posts by a specific author that the current authenticated user
                        # can view
#                       author/id1/posts
                        #  /api/author/ef3e0e05-c5f8-11e4-a972-b8f6b116b2b7/posts/
                        (r'^author/(?:(?P<author_id>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/)?posts/?(?:/(?P<page>\d*))/?$', 'get_posts'),

                       # Get a specific post or all public posts
                       (r'^posts/?(?:(?P<post_id>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}))?/?$', 'get_post'),

                       #See if a author_id is a friend with author_2_id
                       (r'^friends/(?P<author_id>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/(?P<author_2_id>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/?$', 'is_friend'),

                       # POST authors, returns list of friends in the list
                       (r'^friends/(?P<author_id>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/?$', 'get_friends'),
                       # Make a friend request with another user
                       (r'^friendrequest$', 'friend_request'),
)
