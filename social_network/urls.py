from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponse


def test(request):
    return HttpResponse("Hello World")


urlpatterns = patterns('social_network.views',
                       # Examples:
                       # url(r'^$', 'untitled.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^$',
                           test),
                       url(r'^admin/', include(admin.site.urls)),
)
#
# Example of named-group pattern
# urlpatterns = patterns('',
# (r'^articles/(?P<year>\d{4})/$', views.year_archive),
#     (r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/$', views.month_archive),
# )
#
# Example of patterns with optional parameter
# urlpatterns = patterns('',
#     (r'^foo/$', views.foobar_view, {'template_name': 'template1.html'}),
#     (r'^bar/$', views.foobar_view, {'template_name': 'template2.html'}),
# )