"""
This is an example test file.
Notice how the file is prefixed with test_
All definitions are testMATCH as well. nosetests will pick these up and run them automatically.

I'd suggest reading up on more complex examples here:
http://ivory.idyll.org/articles/nose-intro.html

More examples can be found here:
https://nose.readthedocs.org/en/latest/writing_tests.html
"""
import unittest
import sys, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'social_network.test_settings'
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from api.models import Server
from django.contrib.auth.models import User
from user_profile.models import Profile
from posts.models import Post
from django.utils import timezone
from django.core import management

import signal
import subprocess
import time

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

server_process = None
path = os.path.join(BASE_DIR, 'manage.py')

def run_server():
    return

def kill_server(server_process):
    os.killpg(server_process.pid, signal.SIGTERM)  # Send the signal to all the process groups

class ApiTestClass(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        call_command('makemigrations', interactive=False)
        call_command('migrate', interactive=False)
        call_command('syncdb', interactive=False)
        call_command('flush',interactive=False)

        #  Start our server
        self.server_process = subprocess.Popen('python "{}" runserver --setting=social_network.test_settings'.format(path), stdout=subprocess.PIPE,
                       shell=True, preexec_fn=os.setsid,stderr=subprocess.PIPE)

        #call_command("runserver",addr='0.0.0.0', port='8080', use_reloader=False)
        self.test = User.objects.create_user('Test','myemail@email.com','password')
        self.test_profile = Profile.objects.create(author=self.test,display_name="Test User")
        self.post = Post.objects.create(title='randomtitle', date=timezone.now(), text='sometext', image=None,
                                 visibility=Post.public, commonmark=False, author=self.test_profile, origin="localhost", source="localhost")


        # Setup our own server as a "server"
        self.server = Server.objects.create(host="127.0.0.1:8000/api",
            user_header="User",
            auth_type="Basic",
            auth_user="node",
            auth_password="api",
            realm="Realm")

    @classmethod
    def tearDownClass(self):
        print "Killing server"

        # Kill the server
        os.killpg(self.server_process.pid, signal.SIGTERM)  # Send the signal to all the process groups


    def test_server_posts(self):
        print "getting server posts"
        posts = self.server.get_posts()
        self.assertEqual(len(posts),1)
        self.assertEqual('posts' in posts,True)

        # Get first post
        post = posts['posts'][0]
        self.assertEqual(post["visibility"],"PUBLIC")
        self.assertEqual(post["title"],self.post.title)
'''
    def test_server_posts_id(self):
        print server.get_posts_id(post_guid="290da6fd-d3d3-11e4-a23b-b8f6b116b2b7")

    def test_server_friends_id_id(self):
        print server.get_friends_id_id(friend_guid="7a1c7226-d1e4-11e4-aa4c-b8f6b116b2b7",friend_2_guid="290da6fd-d3d3-11e4-a23b-b8f6b116b2b7")

    def test_server_friends_list(self):
        my_list = ['7a1c7226-d1e4-11e4-aa4c-b8f6b116b2b7','e725d1c2-d3d6-11e4-97dc-b8f6b116b2b7','f0e2aec2-d3d6-11e4-8af3-b8f6b116b2b7','0471f261-d3d7-11e4-9922-b8f6b116b2b7']
        response = server.get_friends_list(friend_guid="7a1c7226-d1e4-11e4-aa4c-b8f6b116b2b7",friends_list=my_list)
        print response
'''
