from django.conf.urls import patterns

urlpatterns = patterns('framework.views',
                       (r'^$', 'login'),
                       (r'^login/$', 'login'),
                       (r'^dashboard/$', 'dashboard'),
                       (r'^logout/$', 'logout'),
                       (r'^signup/$', 'signup'),
)
