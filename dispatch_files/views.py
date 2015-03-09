from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from social_network.settings import MEDIA_ROOT
import os

# Create your views here.

@login_required
def images(request, year, month, day, file_name, image_type="JPG"):
    """Returns an image with the mimetype"""

    # TODO: Check here to see if user has access to the image

    with open(os.path.join(MEDIA_ROOT, "images", year, month, day, "{}.{}".format(file_name, image_type)), "rb") as f:
        return HttpResponse(f.read(), content_type="image/{}".format(image_type.lower()))