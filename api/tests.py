from django.contrib.auth.models import AnonymousUser, User
from posts.models import Post
from user_profile.models import Profile
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
        self.user_profile = Profile.objects.create(author=self.user,display_name="Chris")
        self.user2 = User.objects.create_user(
            username='ffff', email='chris@email.com', password='top_secret')
        self.user2_profile = Profile.objects.create(author=self.user2,display_name="FFFF")

    def test_author_posts(self):
        ''' get the current logged in users visible posts '''

        # Factory for get request
        request = self.factory.get('/api/author/posts')

        # Set the user
        request.user = self.user;

        response = get_posts(request)
        json_obj = json.loads(response.content)
        self.assertEqual(json_obj['posts'],[])


    def test_author_posts_id_incorrect(self):
        ''' get the current logged in users visible posts '''

        Post.objects.create(title='randomtitle', date=timezone.now(), text='sometext', image=None,
                                 visibility=Post.friend, commonmark=False, author=self.user, origin="localhost", source="localhost")

        # Factory for get request
        request = self.factory.get('/api/author/%d/posts' % self.user2.id)

        # Set the user
        request.user = self.user;

        response = get_posts(request,self.user2.id)
        json_obj = json.loads(response.content)
        self.assertEqual(json_obj['posts'],[])

    def test_author_posts_id_correct(self):
        ''' get specific authors posts '''

        Post.objects.create(title='randomtitle', date=timezone.now(), text='sometext', image=None,
                                 visibility=Post.friend, commonmark=False, author=self.user, origin="localhost", source="localhost")

        # Factory for get request
        request = self.factory.get('/api/author/%d/posts' % self.user.id)

        # Set the user
        request.user = self.user;

        response = get_posts(request,self.user.id)
        json_obj = json.loads(response.content)
        self.assertEqual(len(json_obj['posts']),1)

    def test_author_posts_id_not_self(self):
        ''' get another users posts'''

        Post.objects.create(title='randomtitlepublic', date=timezone.now(), text='sometext', image=None,
                                 visibility=Post.public, commonmark=False, author=self.user2, origin="localhost", source="localhost")

        Post.objects.create(title='randomtitle', date=timezone.now(), text='sometext', image=None,
                                 visibility=Post.friend, commonmark=False, author=self.user2, origin="localhost", source="localhost")
        Post.objects.create(title='randomtitle', date=timezone.now(), text='sometext', image=None,
                                 visibility=Post.private, commonmark=False, author=self.user2, origin="localhost", source="localhost")
        Post.objects.create(title='randomtitle', date=timezone.now(), text='sometext', image=None,
                                 visibility=Post.FOAF, commonmark=False, author=self.user2, origin="localhost", source="localhost")

        # Factory for get request
        request = self.factory.get('/api/author/%d/posts' % self.user2.id)

        # Set the user
        request.user = self.user;

        response = get_posts(request,self.user2.id)
        json_obj = json.loads(response.content)
        self.assertEqual(len(json_obj['posts']),1)
        self.assertEqual(json_obj['posts'][0]['title'],'randomtitlepublic')

    def test_author_posts_id_doesnot_exist(self):
        ''' try to get a invalid users posts'''

        author_id = 20000

        Post.objects.create(title='randomtitlepublic', date=timezone.now(), text='sometext', image=None,
                                 visibility=Post.public, commonmark=False, author=self.user2, origin="localhost", source="localhost")

        Post.objects.create(title='randomtitle', date=timezone.now(), text='sometext', image=None,
                                 visibility=Post.friend, commonmark=False, author=self.user2, origin="localhost", source="localhost")
        Post.objects.create(title='randomtitle', date=timezone.now(), text='sometext', image=None,
                                 visibility=Post.private, commonmark=False, author=self.user2, origin="localhost", source="localhost")
        Post.objects.create(title='randomtitle', date=timezone.now(), text='sometext', image=None,
                                 visibility=Post.FOAF, commonmark=False, author=self.user2, origin="localhost", source="localhost")

        # Factory for get request
        request = self.factory.get('/api/author/%d/posts' % author_id)

        # Set the user
        request.user = self.user;

        response = get_posts(request,author_id)
        json_obj = json.loads(response.content)
        self.assertEqual(response.status_code,404)
        self.assertEqual(json_obj['message'],"Author with id %d does not exist" % author_id)

    def test_invalid_accept(self):
        ''' try to get with invalid accept '''

        # Factory for get request
        request = self.factory.get('/api/author/%d/posts' % self.user2.id,Accept='html/text')

        # Set the user
        request.user = self.user;

        response = get_posts(request,self.user2.id)
        self.assertEqual(response.status_code,406)


    def test_invalid_accept_2(self):
        ''' try to get with invalid accept '''

        # Factory for get request
        request = self.factory.get('/api/author/posts',Accept='html/text')

        # Set the user
        request.user = self.user;

        response = get_posts(request)
        self.assertEqual(response.status_code,406)
