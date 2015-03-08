from django.conf.urls import patterns, include, url

urlpatterns = patterns('api.views',
                        # get posts that are visible to current authenticated user
                       (r'^author/posts$', 'get_posts'),

                        # get posts by a specific author that the current authenticated user
                        # can view
                       (r'^author/(?P<author_id>[^/]+)/posts$', 'get_posts'),

                       # Get a specific post
                       (r'^posts/(?P<post_id>[^/]+)$', 'get_posts'),

                       #See if a author_id is a friend with author_2_id
                       (r'^friends/(?P<author_id>[^/]+)/(?P<author_2_id>[^/]+)$', 'get_posts'),

                       # POST authors, returns list of friends in the list
                       (r'^friends/(?P<author_id>[^/]+)$', ''),

                       # Make a friend request with another user
                       (r'^friendrequest$', 'friend_request'),
)
