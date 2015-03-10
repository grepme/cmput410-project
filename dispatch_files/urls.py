from django.conf.urls import patterns, include, url

urlpatterns = patterns('dispatch_files.views',
                       (r'(?i)images/(\d{1,4})/(\d{1,2})/(\d{1,2})/([-_.\w]+).JPG$', 'images', {'image_type': "JPG"}),
                       (r'(?i)images/(\d{1,4})/(\d{1,2})/(\d{1,2})/([-_.\w]+).PNG$', 'images', {'image_type': "PNG"}),
                       (r'(?i)images/(\d{1,4})/(\d{1,2})/(\d{1,2})/([-_.\w]+).GIF$', 'images', {'image_type': "GIF"})

)
