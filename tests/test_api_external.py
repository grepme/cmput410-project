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
from django.conf import settings
from user_profile.models import Profile
from friends.models import Friend,Follow
from posts.models import Post
from django.utils import timezone
from django.core import management
from django.http import HttpRequest

import signal
import subprocess, shlex
import time

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

server_process = None
path = os.path.join(BASE_DIR, 'manage.py')

visibilities = ["PUBLIC","FOAF","FRIENDS","PRIVATE","SERVERONLY"]

def check_keys(self,keys,item):
    for key in keys:
        # Check if has key
        self.assertEqual(key in item,True,"Key: '{}' not found in item".format(key))

        if type(item[key]) is str:
            # Make sure key is not empty
            self.assertNotEqual(len(item[key]),0,"Key: '{}' has length 0".format(key))

        # Check for valid visibilities
        check_visibility(self,key,item)

def check_visibility(self,key,item):
    if key == "visibility":
        self.assertEqual(item[key].upper() in visibilities,True,"Visibility is not valid")

def check_url(self,item):
    check_keys(self,['url'],item)
    self.assertTrue(self.server.host in item['url'],"{} not found in {}".format(self.server.host,item['url']))
    self.assertTrue(item['id'] in item['url'])

def check_author(self,author,has_url=False):
    check_keys(self,['id','host','displayname'],author)
    # If we want to check for url
    if has_url:
       check_url(self,author)

def check_comment(self,comment):
    check_keys(self,['author','comment','pubDate','guid'],comment)
    check_author(self,comment["author"])

def check_origin_source(self,item):
    self.assertTrue(self.server.host in item['origin'],"{} not found in {}".format(self.server.host,item['origin']))
    self.assertTrue(self.server.host in item['source'],"{} not found in {}".format(self.server.host,item['source']))



def check_post(self,post):
    # Check that we have all the main keys
    check_keys(self,['title','source','origin','description','content-type'
        ,'content','author','categories','comments','pubDate','guid','visibility'],post)

    # Check if author is valid
    check_author(self,post["author"],True)

    check_origin_source(self,post)

    for comment in post["comments"]:
        check_comment(self,comment)

def check_friends(self,query):
    check_keys(self,['query','author','friends'],query)

def check_profile(self,profile):
    check_author(self,profile,True)
    check_keys(self,['friends'],profile)
    for friend in profile["friends"]:
        check_author(self,friend,True)

def create_user(name):
    user = User.objects.create_user(name,"{}@{}.com".format(name,name),'password')
    profile = Profile.objects.create(author=user,display_name=name)
    return (user,profile)

def create_post(server,title,text,author,visibility):
    return Post.objects.create(title=title, date=timezone.now(), text=text, image=None,
                                 visibility=visibility, commonmark=False, author=author, origin=server.host, source=server.host)


class ApiTestClass(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        p1 = subprocess.Popen(shlex.split("pgrep -f 'manage.py runserver'"), stdout=subprocess.PIPE)
        p2 = subprocess.Popen(shlex.split("xargs kill"), stdin=p1.stdout, stdout=subprocess.PIPE)

        subprocess.Popen(shlex.split('rm "{}"'.format(settings.DATABASES["default"]["NAME"])))
        call_command('makemigrations', interactive=False)
        call_command('migrate', interactive=False)
        call_command('syncdb', interactive=False)
        call_command('flush',interactive=False)

        #  Start our server
        self.server_process = subprocess.Popen(shlex.split('python "{}" runserver --setting=social_network.test_settings'.format(path)))
        time.sleep(2)

        # Setup our own server as a "server"
        self.server = Server.objects.create(host="127.0.0.1:8000",
            api_path="/api",
            user_header="User",
            auth_type="Basic",
            auth_user="node",
            auth_password="api",
            realm="Realm")

        #call_command("runserver",addr='0.0.0.0', port='8080', use_reloader=False)
        user_tuple = create_user("test")
        self.test = user_tuple[0]
        self.test_profile = user_tuple[1]

        user_tuple2 = create_user("test2")
        self.test2 = user_tuple2[0]
        self.test_profile2 = user_tuple2[1]

        self.test_profile3 = Profile.objects.create(display_name="Random Profile",host="http://127.0.0.1:8000",is_external=True)

        self.post = create_post(self.server,'randomtitle','sometext',self.test_profile,Post.public)
        self.post_2 = create_post(self.server,'title','text',self.test_profile,Post.private)

    @classmethod
    def tearDownClass(self):
        print "Killing server"

        # Kill the server
        p1 = subprocess.Popen(shlex.split("pgrep -f 'manage.py runserver'"), stdout=subprocess.PIPE)
        p2 = subprocess.Popen(shlex.split("xargs kill"), stdin=p1.stdout, stdout=subprocess.PIPE)


    def test_server_posts(self):
        '''
            Test for Server get_posts():
            Path: '/api/posts'
        '''
        posts = self.server.get_posts()
        self.assertEqual(len(posts["posts"]),len(Post.objects.filter(visibility=Post.public)))
        for post in posts["posts"]:
            check_post(self,post)
            self.assertEqual(post["visibility"].upper(),"PUBLIC")

    def test_server_get_post(self):
        '''
            Test for Server get_post_id():
            Path: '/api/posts/{post_guid}'
        '''
        posts = self.server.get_posts_id(self.post.guid)
        self.assertEqual(len(posts),1)
        for post in posts["posts"]:
            check_post(self,post)

    def test_server_get_posts_auth(self):
        '''
            Test for Server get_auth_author_posts():
            Path: '/api/author/posts'
        '''
        request = HttpRequest()
        request.profile = self.test_profile

        posts = self.server.get_auth_author_posts(request)

        self.assertEqual(len(posts["posts"]),2)

    def test_server_get_author_posts(self):
        '''
            Test for Server get_author_posts():
            Path: '/api/author/{author_guid}/posts'
        '''
        request = HttpRequest()
        request.profile = self.test_profile2

        posts = self.server.get_author_posts(request, self.test_profile)

        self.assertEqual(len(posts["posts"]),1)

    def test_server_post_friend_request(self):
        '''
            Test for Server post_friend_request():
            Path: '/api/friendrequest'
        '''
        profile = self.test_profile3

        response = self.server.post_friend_request(requester=profile, accepter=self.test_profile)

        self.assertEqual(response,None)

        # Throw error if we cannot find this request
        Friend.objects.get(requester=profile,accepter=self.test_profile,accepted=False)
        Follow.objects.get(follower=profile,following=self.test_profile)

        # Try duplicate requests
        response = self.server.post_friend_request(requester=profile, accepter=self.test_profile)
        self.assertEqual(response,None)
        # Try duplicate requests
        response = self.server.post_friend_request(requester=profile, accepter=self.test_profile)
        self.assertEqual(response,None)

        # Accept the request
        response = self.server.post_friend_request(requester=self.test_profile, accepter=profile)
        self.assertEqual(response,None)

        # Check database for the Request
        Friend.objects.get(requester=profile,accepter=self.test_profile,accepted=True)
        Follow.objects.get(follower=profile,following=self.test_profile)

        # Accept the request
        response = self.server.post_friend_request(requester=self.test_profile, accepter=profile)
        self.assertEqual(response,None)
        # Accept the request
        response = self.server.post_friend_request(requester=self.test_profile, accepter=profile)
        self.assertEqual(response,None)

    def test_server_get_friends_id_id(self):
        response = self.server.get_friends_id_id(friend_guid=self.test_profile.guid,friend_2_guid=self.test_profile3.guid)
        self.assertTrue(response.friends)

    '''def test_server_friends_id_id(self):
        print server.get_friends_id_id(friend_guid="7a1c7226-d1e4-11e4-aa4c-b8f6b116b2b7",friend_2_guid="290da6fd-d3d3-11e4-a23b-b8f6b116b2b7")

    def test_server_friends_list(self):
        my_list = ['7a1c7226-d1e4-11e4-aa4c-b8f6b116b2b7','e725d1c2-d3d6-11e4-97dc-b8f6b116b2b7','f0e2aec2-d3d6-11e4-8af3-b8f6b116b2b7','0471f261-d3d7-11e4-9922-b8f6b116b2b7']
        response = server.get_friends_list(friend_guid="7a1c7226-d1e4-11e4-aa4c-b8f6b116b2b7",friends_list=my_list)
        print response
        '''
