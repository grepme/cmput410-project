from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory

from user_profile.views import profile,user_profile,update_profile
from user_profile.models import Profile
from django.contrib.sessions.middleware import SessionMiddleware

#https://lorinstechblog.wordpress.com/2013/01/07/adding-a-session-to-a-django-request-generated-by-requestfactory/
def add_session_to_request(request):
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()

class UserProfileTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test',email='test@test.com',password='test')
        self.user_profile = Profile.objects.create(author=self.user,display_name="Chris")
        self.user2 = User.objects.create_user(username='test2',email='test@test.com',password='test2')
        self.user2_profile = Profile.objects.create(author=self.user2,display_name="Test name 2")

    def test_get_user_profile_not_logged_in(self):
        ''' test get user profile when not logged in '''
        request = self.factory.get('/profile/test/')
        request.user = AnonymousUser()
        add_session_to_request(request)

        response = profile(request)

        self.assertEqual(response.status_code,302)
        self.assertEqual(response.url,'/login/?next=/profile/test/')

    def test_get_user_profile(self):
        ''' test get user profile '''
        request = self.factory.get('/profile/test/')
        request.user = self.user
        add_session_to_request(request)
        response = profile(request,self.user)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'profile/author.html')

    def test_get_profile(self):
        ''' test get profile '''
        request = self.factory.get('/profile/')
        request.user = self.user
        add_session_to_request(request)
        response = profile(request)
        self.assertEqual(response.status_code,302)
        self.assertEqual(response.url,'/profile/test/')

    def test_other_methods_user_profile(self):
        ''' test other methods user profile when not logged in '''
        request = self.factory.post('/profile/test/')
        request.user = AnonymousUser()
        response = profile(request)
        self.assertEqual(response.status_code,405)

        request = self.factory.delete('/profile/test/')
        request.user = AnonymousUser()
        response = profile(request)
        self.assertEqual(response.status_code,405)

        request = self.factory.put('/profile/test/')
        request.user = AnonymousUser()
        response = profile(request)
        self.assertEqual(response.status_code,405)

    def test_get_profile(self):
        ''' test get profile when not logged in '''
        request = self.factory.get('/profile/')
        request.user = AnonymousUser()
        add_session_to_request(request)

        response = user_profile(request)

        self.assertEqual(response.status_code,302)

    def test_other_methods_profile(self):
        ''' test other methods profile when not logged in '''
        request = self.factory.post('/profile/')
        request.user = AnonymousUser()
        response = profile(request)
        self.assertEqual(response.status_code,405)

        request = self.factory.delete('/profile/')
        request.user = AnonymousUser()
        response = profile(request)
        self.assertEqual(response.status_code,405)

        request = self.factory.put('/profile/')
        request.user = AnonymousUser()
        response = profile(request)
        self.assertEqual(response.status_code,405)

    def test_update_profile(self):
        ''' test update profile when not logged in '''
        request = self.factory.post('/profile/update/')
        request.user = AnonymousUser()
        add_session_to_request(request)

        response = user_profile(request)
        self.assertEqual(response.status_code,302)
        self.assertEqual(response.url,'/login/?next=/profile/update/')

    def test_update_profile_invalid_methods(self):
        ''' test update profile invalid methods when not logged in '''
        request = self.factory.get('/profile/update/')
        request.user = AnonymousUser()
        add_session_to_request(request)
        response = user_profile(request)
        self.assertEqual(response.status_code,405)

        request = self.factory.delete('/profile/update/')
        request.user = AnonymousUser()
        add_session_to_request(request)
        response = user_profile(request)
        self.assertEqual(response.status_code,405)

        request = self.factory.put('/profile/update/')
        request.user = AnonymousUser()
        add_session_to_request(request)
        response = user_profile(request)
        self.assertEqual(response.status_code,405)

        request = self.factory.get('/profile/update/')
        request.user = self.user
        add_session_to_request(request)
        response = user_profile(request)
        self.assertEqual(response.status_code,405)

        request = self.factory.delete('/profile/update/')
        request.user = self.user
        add_session_to_request(request)
        response = user_profile(request)
        self.assertEqual(response.status_code,405)

        request = self.factory.put('/profile/update/')
        request.user = self.user
        add_session_to_request(request)
        response = user_profile(request)
        self.assertEqual(response.status_code,405)

    def test_update_profile_valid(self):
        ''' test update profile when logged in '''
        request = self.factory.post('/profile/update/',{'display_name':'my new display name'})
        request.user = self.user
        add_session_to_request(request)

        response = user_profile(request)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.content,'{"status": true}')
