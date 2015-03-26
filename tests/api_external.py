"""
This is an example test file.
Notice how the file is prefixed with test_
All definitions are testMATCH as well. nosetests will pick these up and run them automatically.

I'd suggest reading up on more complex examples here:
http://ivory.idyll.org/articles/nose-intro.html

More examples can be found here:
https://nose.readthedocs.org/en/latest/writing_tests.html
"""
from django.core.management import setup_environ
from social_network import settings
settings.configure()
import unittest

from api.models import Server

class ApiTestClass(unittest.TestCase):

    def setUp(self):


    def tearDown(self):

    def test_server_posts(self):
        server = Server.objects.create(host="localhost:8000/api",
            user_header="User",
            auth_type="Basic",
            auth_user="node",
            auth_password="api",
            realm="Realm")

        print server.get_posts()

    def test_server_posts_id(self):

        server = Server.objects.create(host="localhost:8000/api",
            user_header="User",
            auth_type="Basic",
            auth_user="node",
            auth_password="api",
            realm="Realm")

        print server.get_posts_id(post_guid="290da6fd-d3d3-11e4-a23b-b8f6b116b2b7")

    def test_server_friends_id_id(self):

        server = Server.objects.create(host="localhost:8000/api",
            user_header="User",
            auth_type="Basic",
            auth_user="node",
            auth_password="api",
            realm="Realm")

        print server.get_friends_id_id(friend_guid="7a1c7226-d1e4-11e4-aa4c-b8f6b116b2b7",friend_2_guid="290da6fd-d3d3-11e4-a23b-b8f6b116b2b7")

    def test_server_friends_list(self):

        server = Server.objects.create(host="localhost:8000/api",
            user_header="User",
            auth_type="Basic",
            auth_user="node",
            auth_password="api",
            realm="Realm")

        my_list = ['7a1c7226-d1e4-11e4-aa4c-b8f6b116b2b7','e725d1c2-d3d6-11e4-97dc-b8f6b116b2b7','f0e2aec2-d3d6-11e4-8af3-b8f6b116b2b7','0471f261-d3d7-11e4-9922-b8f6b116b2b7']

        response = server.get_friends_list(friend_guid="7a1c7226-d1e4-11e4-aa4c-b8f6b116b2b7",friends_list=my_list)
        print response
