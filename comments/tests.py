from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from django.utils import timezone

from posts.views import new_post, delete_post, all_posts, my_posts
from comments.views import new_comment
from posts.models import Post
from comments.models import Comment

class PostsViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test',email='test@test.com',password='test')
        # self.user2 = User.objects.create_user(username='test2',email='test@test.com',password='test2')
        self.post = Post.objects.create(title='a post title', date=timezone.now(), text='sometext', image=None,
                                 visibility=Post.friend, commonmark=False, author=self.user, origin="localhost", source="localhost")
        # self.post2 = Post.objects.create(title='randomtitle2', date=timezone.now(), text='sometext', image=None,
        #                          visibility=Post.friend, commonmark=False, author=self.user2, origin="localhost", source="localhost")
        self.comment = Comment.objects.create(date=timezone.now(), text='commentText', image=None, post=self.post, author=self.user)


    def test_new_comment(self):
        post = Post.objects.get(title=self.post.title)
        ''' Tests if we can add a new comment using the endpoint '''
        request = self.factory.post('/comment/new',{"date":timezone.now(), "text":'new comment text', "image":None,
                                                    "post":post, "author":self.user})
        request.user = self.user

        response = new_comment(request)

        self.assertEqual(response.__class__.__name__,'HttpResponseRedirect')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/dashboard/')