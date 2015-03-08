from django.conf.urls import patterns, include, url

urlpatterns = patterns('dispatch_files.views',
                       (r'images/(\d{1,4})/(\d{1,2})/(\d{1,2})/(\w+).JPG$', 'images', {'type': "JPG"}),
                       (r'images/(\d{1,4})/(\d{1,2})/(\d{1,2})/(\w+).PNG$', 'images', {'type': "PNG"}),
                       (r'images/(\d{1,4})/(\d{1,2})/(\d{1,2})/(\w+).GIF$', 'images', {'type': "GIF"})

)
