from django.conf.urls import patterns
from django.contrib import admin

urlpatterns = patterns('framework.views',
                       (r'^$', 'test'),
)