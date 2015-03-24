from django.utils.functional import SimpleLazyObject
from user_profile.models import Profile

def get_profile(request):
    if not hasattr(request, '_cached_profile'):
        request._cached_profile = Profile.objects.get(author=request.user)
    return request._cached_profile


class ProfileMiddleware(object):
    def process_request(self, request):
        if hasattr(request,'user'):
            request.profile = SimpleLazyObject(lambda: get_profile(request))
