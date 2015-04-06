from django.conf.urls import patterns

urlpatterns = patterns('framework.views',
                       (r'^$', 'login'),
                       (r'^login/$', 'login'),
                       (r'^dashboard/$', 'dashboard'),
                       (r'^logout/$', 'logout'),
                       (r'^signup/$', 'signup'),
)

from django.conf import settings

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'%s(?P<path>.*)' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
