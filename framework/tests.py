from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory

from framework.views import login, dashboard, logout, signup
from django.contrib.sessions.middleware import SessionMiddleware

# Create your tests here.

# https://lorinstechblog.wordpress.com/2013/01/07/adding-a-session-to-a-django-request-generated-by-requestfactory/
def add_session_to_request(request):
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()


class FrameWorkViewTests(TestCase):
    def setUp(self):
        # Factory for requests
        self.factory = RequestFactory()

        # create some users
        self.user = User.objects.create_user(username='test', email='test@test.com', password='test')

        # Dummy User
        self.fake_user = User(username='fake', email='fake@test.com', password='fake')

    def test_login_valid(self):
        ''' test login with valid user '''
        request = self.factory.post('/login/', {'username': 'test', 'password': 'test'})
        request.user = AnonymousUser()
        add_session_to_request(request)

        response = login(request)
        self.assertEqual(response.__class__.__name__, 'HttpResponseRedirect')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/dashboard/')

    def test_login_invalid(self):
        ''' test login with invalid user '''
        request = self.factory.get('/login/', {'username': 'fake', 'password': 'doesntmatter'})
        request.user = AnonymousUser()
        add_session_to_request(request)

        response = login(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'framework/login.html')

    def test_logout(self):
        ''' test logout '''
        request = self.factory.get('/logout/');
        request.user = self.user
        add_session_to_request(request)

        response = logout(request)

        self.assertTemplateUsed(response, 'framework/login.html')

    def test_signup_valid(self):
        ''' test valid signup '''
        request = self.factory.post('/signup/', {'signupUsername': 'newUser', 'signupPassword': 'newPass',
                                                 'signupDuplicatePassword': 'newPass',
                                                 'signupEmail': 'test@here.com', 'signupFirstName': 'John',
                                                 'signupLastName': 'doe'})
        request.user = AnonymousUser()
        add_session_to_request(request)

        response = signup(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/dashboard/')

    def test_signup_already_logged_in(self):
        ''' test sign up if already logged in '''
        request = self.factory.post('/signup/', {'signupUsername': 'test', 'signupPassword': 'test',
                                                 'signupDuplicatePassword': 'test',
                                                 'signupEmail': 'test@here.com', 'signupFirstName': 'John',
                                                 'signupLastName': 'doe'})
        request.user = self.user
        add_session_to_request(request)

        response = login(request)
        self.assertEqual(response.__class__.__name__, 'HttpResponseRedirect')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/dashboard/')

    def test_signup_invalid_username(self):
        ''' test signup without username '''
        request = self.factory.post('/signup/', {'signupUsername': '', 'signupPassword': 'newPass',
                                                 'signupDuplicatePassword': 'newPass',
                                                 'signupEmail': 'test@here.com', 'signupFirstName': 'John',
                                                 'signupLastName': 'doe'})
        request.user = AnonymousUser()
        add_session_to_request(request)

        response = signup(request)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.url, '/signup/')

    def test_signup_invalid_password(self):
        ''' test singup without password'''
        request = self.factory.post('/signup/', {'signupUsername': 'aValidName', 'signupPassword': '',
                                                 'signupDuplicatePassword': '',
                                                 'signupEmail': 'test@here.com', 'signupFirstName': 'John',
                                                 'signupLastName': 'doe'})
        request.user = AnonymousUser()
        add_session_to_request(request)

        response = signup(request)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.url, '/signup/')

    def test_signup_invalid_email(self):
        ''' test signup with (obviously) bad email '''
        request = self.factory.post('/signup/', {'signupUsername': 'AlsoValid', 'signupPassword': 'newPass',
                                                 'signupDuplicatePassword': 'newPass',
                                                 'signupEmail': 'hasNoAtSign', 'signupFirstName': 'John',
                                                 'signupLastName': 'doe'})
        request.user = AnonymousUser()
        add_session_to_request(request)

        response = signup(request)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.url, '/signup/')

    def test_signup_invalid_firstName(self):
        ''' test signup without first name'''
        request = self.factory.post('/signup/', {'signupUsername': 'validHereToo', 'signupPassword': 'newPass',
                                                 'signupDuplicatePassword': 'newPass',
                                                 'signupEmail': 'test@here.com', 'signupFirstName': '',
                                                 'signupLastName': 'doe'})
        request.user = AnonymousUser()
        add_session_to_request(request)

        response = signup(request)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.url, '/signup/')

    def test_signup_invalid_lastName(self):
        ''' test singup without last name'''
        request = self.factory.post('/signup/', {'signupUsername': 'AlsoAValidUsername', 'signupPassword': 'newPass',
                                                 'signupDuplicatePassword': 'newPass',
                                                 'signupEmail': 'test@here.com', 'signupFirstName': 'John',
                                                 'signupLastName': ''})
        request.user = AnonymousUser()
        add_session_to_request(request)

        response = signup(request)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.url, '/signup/')

    def test_signup_userName_in_use(self):
        ''' test signup with existing username'''
        request = self.factory.post('/signup/', {'signupUsername': 'test', 'signupPassword': 'newPass',
                                                 'signupDuplicatePassword': 'newPass',
                                                 'signupEmail': 'test@here.com', 'signupFirstName': 'John',
                                                 'signupLastName': 'doe'})
        request.user = AnonymousUser()
        add_session_to_request(request)

        response = signup(request)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.url, '/signup/')

    def test_signup_mismatched_passwords(self):
        ''' test signup with mismatching passwords '''
        request = self.factory.post('/signup/', {'signupUsername': 'uniqueName', 'signupPassword': 'newPass',
                                                 'signupDuplicatePassword': 'wrongPass',
                                                 'signupEmail': 'test@here.com', 'signupFirstName': 'John',
                                                 'signupLastName': 'doe'})
        request.user = AnonymousUser()
        add_session_to_request(request)

        response = signup(request)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.url, '/signup/')

    ''' This is an odd case, what should it actually do? '''
    def test_signup_again(self):
        ''' test signup again with created user '''
        request = self.factory.post('/signup/', {'signupUsername': 'test', 'signupPassword': 'test@test.com',
                                                 'signupDuplicatePassword': 'test@test.com',
                                                 'signupEmail': 'test@here.com', 'signupFirstName': 'John',
                                                 'signupLastName': 'doe'})
        request.user = AnonymousUser()
        add_session_to_request(request)

        response = signup(request)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.url, '/signup/')