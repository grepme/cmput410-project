from django.conf.urls import patterns, include, url

urlpatterns = patterns('dispatch_files.views',
                       (r'images/(\d{1,4})/(\d{1,2})/(\d{1,2})/(\w+).JPG$', 'images', {'image_type': "JPG"}),
                       (r'images/(\d{1,4})/(\d{1,2})/(\d{1,2})/(\w+).PNG$', 'images', {'image_type': "PNG"}),
                       (r'images/(\d{1,4})/(\d{1,2})/(\d{1,2})/(\w+).GIF$', 'images', {'image_type': "GIF"})

)
