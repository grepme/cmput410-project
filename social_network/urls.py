from django.conf.urls import patterns, include, url
from django.contrib import admin

# Import the urls from our apps
import framework.urls
import user_profile.urls
import friends.urls
import api.urls
import posts.urls
import comments.urls
import dispatch_files.urls

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'untitled.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       (r'^', include(framework.urls)),
                       (r'^api/', include(api.urls)),
                       (r'^profile/', include(user_profile.urls)),
                       (r'^admin/', include(admin.site.urls)),
                       (r'^post/', include(posts.urls)),
                       (r'^comment/', include(comments.urls)),
                       (r'^friends/', include(friends.urls)),
                       (r'^uploads/', include(dispatch_files.urls)),
)
#
# Example of named-group pattern
# urlpatterns = patterns('',
# (r'^articles/(?P<year>\d{4})/$', views.year_archive),
# (r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/$', views.month_archive),
# )
#
# Example of patterns with optional parameter
# urlpatterns = patterns('',
# (r'^foo/$', views.foobar_view, {'template_name': 'template1.html'}),
#     (r'^bar/$', views.foobar_view, {'template_name': 'template2.html'}),
# )
