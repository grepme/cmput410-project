from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory

from posts.views import new_post, delete_post, all_posts, my_posts
from posts.models import Post

class PostsViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test',email='test@test.com',password='test')

    def test_new_post(self):
        request = self.factory.post('/post/new',{'title':'my new title', 'content_type':'text','visibility':'Public'})
        request.user = self.user

        response = new_post(request)

        self.assertEqual(response.__class__.__name__,'HttpResponseRedirect')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/dashboard/')

        self.assertEqual(len(Post.objects.filter(title='my new title')),1)

    def test_new_post_wrong_type(self):
        request = self.factory.get('/post/new')
        request.user = self.user

        response = new_post(request)

        self.assertEqual(response.__class__.__name__,'HttpResponseRedirect')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

