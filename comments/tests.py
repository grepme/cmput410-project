from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from django.utils import timezone

from comments.views import new_comment
from posts.models import Post
from comments.models import Comment
from user_profile.models import Profile

class PostsViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test',email='test@test.com',password='test')
        self.user_profile = Profile.objects.create(author=self.user,display_name="DISPLAY")
        # self.user2 = User.objects.create_user(username='test2',email='test@test.com',password='test2')
        self.post = Post.objects.create(title='a post title', date=timezone.now(), text='sometext', image=None,
                                 visibility=Post.friend, commonmark=False, author=self.user_profile, origin="localhost", source="localhost")
        # self.post2 = Post.objects.create(title='randomtitle2', date=timezone.now(), text='sometext', image=None,
        #                          visibility=Post.friend, commonmark=False, author=self.user2, origin="localhost", source="localhost")
        self.comment = Comment.objects.create(date=timezone.now(), text='justAtest', image=None, post=self.post, author=self.user_profile)


    def test_new_comment(self):
        ''' Tests if we can add a new comment using the endpoint '''
        request = self.factory.post('/comment/new',{"date":timezone.now(), "text":'new comment text', "image":None,
                                                    "post":self.post, 'post_id':self.post.guid})
        request.user = self.user
        request.profile = self.user_profile

        response = new_comment(request)

        self.assertEqual(response.__class__.__name__,'HttpResponseRedirect')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/dashboard/')

        self.assertEqual(len(Comment.objects.filter(text='new comment text')),1)

    def test_new_comment_wrong_Type(self):
        ''' test 405 responses for method not allowed '''

        request = self.factory.get('/comment/new')
        request.user = self.user
        request.profile = self.user_profile
        response = new_comment(request)
        self.assertEqual(response.status_code, 405)

        request = self.factory.delete('/comment/new')
        request.user = self.user
        request.profile = self.user_profile
        response = new_comment(request)
        self.assertEqual(response.status_code, 405)

        request = self.factory.put('/comment/new')
        request.user = self.user
        request.profile = self.user_profile
        response = new_comment(request)
        self.assertEqual(response.status_code, 405)

    #TODO: Delete comments? Authentication tests?
