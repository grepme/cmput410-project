from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory

from framework.views import login,dashboard,logout
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sessions.middleware import SessionMiddleware

# Create your tests here.

#https://lorinstechblog.wordpress.com/2013/01/07/adding-a-session-to-a-django-request-generated-by-requestfactory/
def add_session_to_request(request):
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()

class FrameWorkViewTests(TestCase):
    def setUp(self):
        # Factory for requests
        self.factory = RequestFactory()

        # create some users
        self.user = User.objects.create_user(username='test',email='test@test.com',password='test')

        # Dummy User
        self.fake_user = User(username='fake',email='fake@test.com',password='fake')

    def test_login_valid(self):
        ''' test login with valid user '''
        request = self.factory.post('/login/',{'username': 'test','password':'test'})
        request.user = AnonymousUser()
        add_session_to_request(request)

        response = login(request)
        self.assertEqual(response.__class__.__name__,'HttpResponseRedirect')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/dashboard/')

    def test_login_invalid(self):
        ''' test login with invalid user '''
        request = self.factory.get('/login/',{'username': 'fake','password':'doesntmatter'})
        request.user = AnonymousUser()
        add_session_to_request(request)

        response = login(request)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'framework/login.html')

    def test_logout(self):
        ''' test logout '''
        request = self.factory.get('/logout/');
        request.user = self.user
        add_session_to_request(request)

        response = logout(request)

        self.assertTemplateUsed(response,'framework/login.html')


