from django.contrib.auth.models import AnonymousUser, User
from user_profile.models import Profile
from django.test import TestCase, RequestFactory
from django.db import IntegrityError
from django.utils import timezone

from uuid import UUID

from posts.views import new_post, delete_post, all_posts, my_posts
from posts.models import Post


class PostsViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test',email='test@test.com',password='test')
        self.user2 = User.objects.create_user(username='test2',email='test@test.com',password='test2')
        self.profile = Profile.objects.create(author=self.user,display_name="USER")
        self.profile2 = Profile.objects.create(author=self.user2,display_name="USER2")
        self.post = Post.objects.create(title='randomtitle', date=timezone.now(), text='sometext', image=None,
                                 visibility=Post.friend, commonmark=False, author=self.profile, origin="localhost", source="localhost")
        self.post2 = Post.objects.create(title='randomtitle2', date=timezone.now(), text='sometext', image=None,
                                 visibility=Post.friend, commonmark=False, author=self.profile2, origin="localhost", source="localhost")

    def test_new_post(self):
        ''' Tests if we can add a new post using the endpoint '''
        request = self.factory.post('/post/new',{'title':'my new title', 'content_type':'text','visibility':'Public'})
        request.user = self.user
        request.profile = self.profile

        response = new_post(request)

        self.assertEqual(response.__class__.__name__,'HttpResponseRedirect')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/dashboard/')

        self.assertEqual(len(Post.objects.filter(title='my new title')),1)

    def test_new_post_invalid_field(self):
        ''' Tests model to see if we can add a new post with an invalid visibility '''
        invalid_field = timezone.now()
        request = self.factory.post('/post/new',{'title':'valid title', 'content_type':'text',
                                                 'visibility':invalid_field})
        request.user = self.user
        request.profile = self.profile
        response = new_post(request)
        self.assertEqual(response.status_code, 400)

    def test_new_post_wrong_methods(self):
        ''' tests if we can do a get to create a new post we should not'''
        request = self.factory.get('/post/new')
        request.user = self.user
        request.profile = self.profile
        response = new_post(request)
        self.assertEqual(response.status_code, 405)

        request = self.factory.delete('/post/new')
        request.user = self.user
        request.profile = self.profile
        response = new_post(request)
        self.assertEqual(response.status_code, 405)

        request = self.factory.put('/post/new')
        request.user = self.user
        request.profile = self.profile
        response = new_post(request)
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        ''' Test deleting a post that the user has access to '''
        request = self.factory.delete('/post/delete/')
        request.user = self.user
        request.profile = self.profile

        response = delete_post(request,self.post.guid)

        self.assertEqual(response.__class__.__name__,'HttpResponseRedirect')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/dashboard/')

        self.assertEqual(len(Post.objects.filter(guid=self.post.guid)),0)

    def test_delete_nonexistent(self):
        ''' Test deleting a post that does not exist '''
        request = self.factory.delete('/post/delete/')
        request.user = self.user
        request.profile = self.profile
        self.post.guid = UUID('{12345678-1234-5678-1234-567812345678}')

        response = delete_post(request,self.post.guid)

        self.assertEqual(response.__class__.__name__,'HttpResponseRedirect')
        self.assertEqual(response.status_code, 404)

        self.assertEqual(len(Post.objects.filter(guid=self.post.guid)),0)

    def test_delete_unauthorized(self):
        ''' Test deleting a post that the user does not have access to '''
        request = self.factory.delete('/post/delete/')
        request.user = self.user
        request.profile = self.profile

        response = delete_post(request,self.post2.guid)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(len(Post.objects.filter(guid=self.post2.guid)),1)

    def test_delete_wrong_methods(self):
        request = self.factory.post('/post/delete/')
        request.user = self.user
        request.profile = self.profile
        response = delete_post(request,self.post.guid)
        self.assertEqual(response.status_code, 405)

        request = self.factory.get('/post/delete/')
        request.user = self.user
        request.profile = self.profile
        response = delete_post(request,self.post.guid)
        self.assertEqual(response.status_code, 405)

        request = self.factory.put('/post/delete/')
        request.user = self.user
        request.profile = self.profile
        response = delete_post(request,self.post.guid)
        self.assertEqual(response.status_code, 405)

        self.assertEqual(len(Post.objects.filter(guid=self.post.guid)),1)

    def test_get_all_posts(self):
        ''' Test getting all of the users posts '''
        request = self.factory.get('/post/all/')
        request.user = self.user
        request.profile = self.profile

        response = all_posts(request)

        #TODO : TEST THIS BETTER, CHECK THAT ALL POSTS WHERE LOADED...

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'post/all.html')

    def test_get_all_posts_unauthorized(self):
        ''' Test getting all posts while not logged in '''
        request = self.factory.get('/post/all/')
        request.user = AnonymousUser()
        response = all_posts(request)

        #TODO : TEST THIS BETTER, CHECK THAT ALL POSTS WHERE LOADED...

        # Should this be 200? Can we see public without account?
        self.assertEqual(response.status_code, 200)

    def test_other_all_posts(self):
        ''' Test getting all of the users posts with wrong methods '''
        request = self.factory.post('/post/all/')
        request.user = self.user
        request.profile = self.profile
        response = all_posts(request)
        self.assertEqual(response.status_code, 405)

        request = self.factory.delete('/post/all/')
        request.user = self.user
        request.profile = self.profile
        response = all_posts(request)
        self.assertEqual(response.status_code, 405)

        request = self.factory.put('/post/all/')
        request.user = self.user
        request.profile = self.profile
        response = all_posts(request)
        self.assertEqual(response.status_code, 405)

    def test_get_my_posts(self):
        ''' Test getting my posts for the current user '''
        request = self.factory.get('/post/all/')
        request.user = self.user
        request.profile = self.profile

        response = my_posts(request)

        #TODO : TEST THIS BETTER, CHECK THAT ALL POSTS WHERE LOADED...

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'post/all.html')

    def test_other_my_posts(self):
        ''' Test getting my users posts with wrong methods '''
        request = self.factory.post('/post/my/')
        request.user = self.user
        request.profile = self.profile
        response = my_posts(request)
        self.assertEqual(response.status_code, 405)

        request = self.factory.delete('/post/my/')
        request.user = self.user
        request.profile = self.profile
        response = my_posts(request)
        self.assertEqual(response.status_code, 405)

        request = self.factory.put('/post/my/')
        request.user = self.user
        request.profile = self.profile
        response = my_posts(request)
        self.assertEqual(response.status_code, 405)
