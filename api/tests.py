from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
# create an instance of the client for our use
# Create your tests here.

from api.views import get_posts

class ApiViewTests(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='chris', email='chris@email.com', password='top_secret')

    def test_author_posts(self):
        ''' get the current logged in users visible posts '''

        # Factory for get request
        request = self.factory.get('/api/author/posts')

        # Set the user
        request.user = self.user;

        response = get_posts(request)
        print (response)

