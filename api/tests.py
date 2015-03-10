from django.contrib.auth.models import AnonymousUser, User
from posts.models import Post
from django.test import TestCase, RequestFactory
from django.utils import timezone
import json
# create an instance of the client for our use
# Create your tests here.

from api.views import get_posts,get_post

class ApiViewTests(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='chris', email='chris@email.com', password='top_secret')
        self.user2 = User.objects.create_user(
            username='ffff', email='chris@email.com', password='top_secret')

    def test_author_posts(self):
        ''' get the current logged in users visible posts '''

        # Factory for get request
        request = self.factory.get('/api/author/posts')

        # Set the user
        request.user = self.user;

        response = get_posts(request)
        json_obj = json.loads(response.content)
        self.assertEqual(json_obj['posts'],u'[]')


    def test_author_posts_id(self):
        ''' get the current logged in users visible posts '''

        Post.objects.create(title='randomtitle', date=timezone.now(), text='sometext', image=None,
                                 visibility=Post.friend, commonmark=False, author=self.user, origin="localhost", source="localhost")

        # Factory for get request
        request = self.factory.get('/api/author/%d/posts' % self.user.id)
        print('/api/author/%d/posts' % self.user2.id)

        # Set the user
        request.user = self.user;

        response = get_posts(request,self.user.id)
        print (response)
