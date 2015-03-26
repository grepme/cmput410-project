from django.contrib.auth.models import AnonymousUser, User
from django.db.models import Q
from posts.models import Post
from friends.models import Friend, Follow
from user_profile.models import Profile
from django.test import TestCase, RequestFactory
from django.utils import timezone
import json
import uuid
# create an instance of the client for our use
# Create your tests here.

from api.views import get_posts,get_post,friend_request,is_friend,get_friends

class ApiViewTests(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='chris', email='chris@email.com', password='top_secret')
        self.user_profile = Profile.objects.create(author=self.user,display_name="Chris")
        self.user2 = User.objects.create_user(
            username='ffff', email='chris@email.com', password='top_secret')
        self.user_profile2 = Profile.objects.create(author=self.user2,display_name="FFFF")

    def test_author_posts(self):
        ''' get the current logged in users visible posts '''

        # Factory for get request
        request = self.factory.get('/api/author/posts')

        # Set the user
        request.user = self.user;
        request.profile = self.user_profile;

        response = get_posts(request)
        json_obj = json.loads(response.content)
        self.assertEqual(json_obj['posts'],[])

    def test_methods_author_posts(self):
        ''' make sure we cant wrong methods '''

        # Factory for get request
        request = self.factory.post('/api/author/posts')
        request.user = self.user;
        request.profile = self.user_profile;
        response = get_posts(request)
        self.assertEqual(response.status_code,405)

        request = self.factory.delete('/api/author/posts')
        request.user = self.user;
        request.profile = self.user_profile;
        response = get_posts(request)
        self.assertEqual(response.status_code,405)

        request = self.factory.put('/api/author/posts')
        request.user = self.user;
        request.profile = self.user_profile;
        response = get_posts(request)
        self.assertEqual(response.status_code,405)


    def test_author_posts_id_incorrect(self):
        ''' get the current logged in users visible posts '''

        Post.objects.create(title='randomtitle', date=timezone.now(), text='sometext', image=None,
                                 visibility=Post.friend, commonmark=False, author=self.user_profile, origin="localhost", source="localhost")

        # Factory for get request
        request = self.factory.get('/api/author/{}/posts'.format(self.user2.id))

        # Set the user
        request.user = self.user;
        request.profile = self.user_profile;

        response = get_posts(request,self.user_profile2.guid)
        json_obj = json.loads(response.content)
        self.assertEqual(json_obj['posts'],[])

    def test_author_posts_id_correct(self):
        ''' get specific authors posts '''

        Post.objects.create(title='randomtitle', date=timezone.now(), text='sometext', image=None,
                                 visibility=Post.friend, commonmark=False, author=self.user_profile, origin="localhost", source="localhost")

        # Factory for get request
        request = self.factory.get('/api/author/{}/posts'.format(self.user_profile.guid))

        # Set the user
        request.user = self.user;
        request.profile = self.user_profile;

        response = get_posts(request,self.user_profile.guid)
        json_obj = json.loads(response.content)
        self.assertEqual(len(json_obj['posts']),1)

    def test_author_posts_id_not_self(self):
        ''' get another users posts'''

        Post.objects.create(title='randomtitlepublic', date=timezone.now(), text='sometext', image=None,
                                 visibility=Post.public, commonmark=False, author=self.user_profile2, origin="localhost", source="localhost")

        Post.objects.create(title='randomtitle', date=timezone.now(), text='sometext', image=None,
                                 visibility=Post.friend, commonmark=False, author=self.user_profile2, origin="localhost", source="localhost")
        Post.objects.create(title='randomtitle', date=timezone.now(), text='sometext', image=None,
                                 visibility=Post.private, commonmark=False, author=self.user_profile2, origin="localhost", source="localhost")
        Post.objects.create(title='randomtitle', date=timezone.now(), text='sometext', image=None,
                                 visibility=Post.FOAF, commonmark=False, author=self.user_profile2, origin="localhost", source="localhost")

        # Factory for get request
        request = self.factory.get('/api/author/{}/posts'.format(self.user_profile2.guid))

        # Set the user
        request.user = self.user;
        request.profile = self.user_profile;

        response = get_posts(request,self.user_profile2.guid)
        json_obj = json.loads(response.content)
        self.assertEqual(len(json_obj['posts']),1)
        self.assertEqual(json_obj['posts'][0]['title'],'randomtitlepublic')

    def test_author_posts_id_doesnot_exist(self):
        ''' try to get a invalid users posts'''

        author_id = 20000

        Post.objects.create(title='randomtitlepublic', date=timezone.now(), text='sometext', image=None,
                                 visibility=Post.public, commonmark=False, author=self.user_profile2, origin="localhost", source="localhost")

        Post.objects.create(title='randomtitle', date=timezone.now(), text='sometext', image=None,
                                 visibility=Post.friend, commonmark=False, author=self.user_profile2, origin="localhost", source="localhost")
        Post.objects.create(title='randomtitle', date=timezone.now(), text='sometext', image=None,
                                 visibility=Post.private, commonmark=False, author=self.user_profile2, origin="localhost", source="localhost")
        Post.objects.create(title='randomtitle', date=timezone.now(), text='sometext', image=None,
                                 visibility=Post.FOAF, commonmark=False, author=self.user_profile2, origin="localhost", source="localhost")

        # Factory for get request
        request = self.factory.get('/api/author/{}/posts'.format(author_id))

        # Set the user
        request.user = self.user;
        request.profile = self.user_profile;

        response = get_posts(request,author_id)
        json_obj = json.loads(response.content)
        self.assertEqual(response.status_code,404)
        self.assertEqual(json_obj['message'],"Author with id {} does not exist".format(author_id))

    def test_invalid_accept(self):
        ''' try to get with invalid accept '''

        # Factory for get request
        request = self.factory.get('/api/author/%s/posts' % self.user_profile2.guid,Accept='html/text')

        # Set the user
        request.user = self.user;
        request.profile = self.user_profile;

        response = get_posts(request,self.user_profile2.guid)
        self.assertEqual(response.status_code,406)


    def test_invalid_accept_2(self):
        ''' try to get with invalid accept '''

        # Factory for get request
        request = self.factory.get('/api/author/posts',Accept='html/text')

        # Set the user
        request.user = self.user;
        request.profile = self.user_profile;

        response = get_posts(request)
        self.assertEqual(response.status_code,406)
    # TODO: Uncomment
    # def test_invalid_accept_api_posts(self):
    #     ''' try to get with invalid accept /api/posts'''
    #
    #     # Factory for get request
    #     request = self.factory.get('/api/posts',Accept='html/text')
    #
    #     # Set the user
    #     request.user = self.user;
    #     request.profile = self.user_profile;
    #     response = get_post(request)
    #     self.assertEqual(response.status_code,406)
    #TODO: Uncomment
    # def test_invalid_accept_api_posts_id(self):
    #     post_id = uuid.uuid1().__str__()
    #     ''' try to get with invalid accept /api/posts/200'''
    #
    #     # Factory for get request
    #     request = self.factory.get('/api/posts/{}'.format(post_id,Accept='html/text'))
    #
    #     # Set the user
    #     request.user = self.user
    #     request.profile = self.user_profile
    #     response = get_post(request,post_id)
    #     print response
    #     self.assertEqual(response.status_code,406)


    def test_methods_posts(self):
        ''' make sure we cant wrong methods '''

        # Factory for get request
        request = self.factory.post('/api/posts')
        request.user = self.user;
        request.profile = self.user_profile;
        response = get_posts(request)
        self.assertEqual(response.status_code,405)

        request = self.factory.delete('/api/posts')
        request.user = self.user;
        request.profile = self.user_profile;
        response = get_posts(request)
        self.assertEqual(response.status_code,405)

        request = self.factory.put('/api/posts')
        request.user = self.user;
        request.profile = self.user_profile;
        response = get_posts(request)
        self.assertEqual(response.status_code,405)

    def test_post_id_doesnot_exist(self):
        ''' try to get a invalid post'''

        post_id = uuid.uuid1().__str__()

        Post.objects.create(title='randomtitlepublic', date=timezone.now(), text='sometext', image=None,
                                 visibility=Post.public, commonmark=False, author=self.user_profile2, origin="localhost", source="localhost")

        # Factory for get request
        request = self.factory.get('/api/posts/%s/' % post_id )

        # Set the user
        request.user = self.user;
        request.profile = self.user_profile;

        response = get_post(request,post_id)
        json_obj = json.loads(response.content)
        self.assertEqual(response.status_code,404)
        self.assertEqual(json_obj['message'],"Post with id {} does not exist".format(post_id))

    def test_post_id_exist(self):
        ''' try to get a post'''

        post = Post.objects.create(title='randomtitlepublic', date=timezone.now(), text='sometext', image=None,
                                 visibility=Post.public, commonmark=False, author=self.user_profile2, origin="localhost", source="localhost")

        # Factory for get request
        request = self.factory.get('/api/posts/{}/'.format(post.guid))

        # Set the user
        request.user = self.user;
        request.profile = self.user_profile;

        response = get_post(request,post.guid)
        json_obj = json.loads(response.content)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(json_obj['posts']),1)

    # def test_send_friendrequest(self):
    #     ''' try to make a friend request '''

    #     authorId = self.user_profile.guid
    #     authorName = self.user_profile.display_name
    #     friendId = self.user_profile2.guid
    #     friendName = self.user_profile2.display_name

    #     # self.user_profile.host = "http://127.0.0.1:8000/"
    #     authorHost = self.user_profile.host
    #     friendHost = self.user_profile2.host
    #     # user_profile doesn't have a url...
    #     authorUrl = "http://localhost:8000/author/"
    #     friendUrl = "http://localhost:8000/author/"+friendId

    #     request_dict = {"author[id]":authorId,"author[displayname]":authorName, "author[host]":authorHost, "author[url]":authorUrl,
    #                    "friend[id]":friendId,"friend[displayname]":friendName, "friend[host]":friendHost, "friend[url]":friendUrl}
    #     request = self.factory.post('/api/friendrequest/', request_dict)

    #     # make sure it doesn't already exist
    #     found = Friend.objects.filter(requester_id=authorId).first()
    #     self.assertIsNone(found)

    #     response = friend_request(request)
    #     found = Friend.objects.filter(Q(requester_id=authorId,accepter_id=friendId) | Q(requester_id=friendId,accepter_id=authorId)).first()
    #     self.assertEqual(response.status_code,201)
    #     self.assertIsNotNone(found)

    # def test_autofollow_friendrequest(self):
    #     ''' ensure friend request autofollows '''

    #     authorId = self.user_profile.guid
    #     authorName = self.user_profile.display_name
    #     friendId = self.user_profile2.guid
    #     friendName = self.user_profile2.display_name

    #     # self.user_profile.host = "http://127.0.0.1:8000/"
    #     authorHost = self.user_profile.host
    #     friendHost = self.user_profile2.host
    #     # user_profile doesn't have a url...
    #     authorUrl = "http://localhost:8000/author/"
    #     friendUrl = "http://localhost:8000/author/"+friendId

    #     request_dict = {"author[id]":authorId,"author[displayname]":authorName, "author[host]":authorHost, "author[url]":authorUrl,
    #                    "friend[id]":friendId,"friend[displayname]":friendName, "friend[host]":friendHost, "friend[url]":friendUrl}
    #     request = self.factory.post('/api/friendrequest/', request_dict)

    #     # make sure it doesn't already exist
    #     follower = Follow.objects.filter(follower_id=authorId).first()
    #     self.assertIsNone(follower)

    #     response = friend_request(request)
    #     follower = Follow.objects.filter(Q(follower_id=authorId, following_id=friendId)).first()
    #     self.assertEqual(response.status_code,201)
    #     self.assertIsNotNone(follower)

    # def test_send_duplicate_friendrequest(self):
    #     ''' make a duplicate friend request '''

    #     authorId = self.user_profile.guid
    #     authorName = self.user_profile.display_name
    #     friendId = self.user_profile2.guid
    #     friendName = self.user_profile2.display_name

    #     # self.user_profile.host = "http://127.0.0.1:8000/"
    #     authorHost = self.user_profile.host
    #     friendHost = self.user_profile2.host
    #     # user_profile doesn't have a url...
    #     authorUrl = "http://localhost:8000/author/"
    #     friendUrl = "http://localhost:8000/author/"+friendId

    #     request_dict = {"author[id]":authorId,"author[displayname]":authorName, "author[host]":authorHost, "author[url]":authorUrl,
    #                    "friend[id]":friendId,"friend[displayname]":friendName, "friend[host]":friendHost, "friend[url]":friendUrl}
    #     request = self.factory.post('/api/friendrequest/', request_dict)

    #     # make sure it doesn't already exist
    #     found = Friend.objects.filter(requester_id=authorId).first()
    #     self.assertIsNone(found)

    #     response = friend_request(request)
    #     response = friend_request(request)
    #     # check that duplicate didn't accept wrongfully
    #     found = Friend.objects.filter(Q(requester_id=authorId,accepter_id=friendId, accepted=False) |
    #                                   Q(requester_id=friendId,accepter_id=authorId, accepted=False)).first()
    #     self.assertEqual(response.status_code, 200)
    #     self.assertNotEqual(response.status_code, 200)
    #     # TODO: Find a better status code check
    #     self.assertIsNotNone(found)

    # def test_complete_friendrequest(self):
    #     ''' make a duplicate friend request '''

    #     authorId = self.user_profile.guid
    #     authorName = self.user_profile.display_name
    #     friendId = self.user_profile2.guid
    #     friendName = self.user_profile2.display_name

    #     # self.user_profile.host = "http://127.0.0.1:8000/"
    #     authorHost = self.user_profile.host
    #     friendHost = self.user_profile2.host
    #     # user_profile doesn't have a url...
    #     authorUrl = "http://localhost:8000/author/"
    #     friendUrl = "http://localhost:8000/author/"+friendId

    #     request_dict = {"author[id]":authorId,"author[displayname]":authorName, "author[host]":authorHost, "author[url]":authorUrl,
    #                    "friend[id]":friendId,"friend[displayname]":friendName, "friend[host]":friendHost, "friend[url]":friendUrl}
    #     request = self.factory.post('/api/friendrequest/', request_dict)

    #     response = friend_request(request)

    #     # make sure it is not already accepted
    #     found = Friend.objects.filter(Q(requester_id=authorId,accepter_id=friendId, accepted=True) |
    #                                   Q(requester_id=friendId,accepter_id=authorId, accepted=True)).first()
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsNone(found)

    #     request_dict = {"author[id]":friendId,"author[displayname]":friendName, "author[host]":friendHost, "author[url]":friendUrl,
    #                    "friend[id]":authorId,"friend[displayname]":authorName, "friend[host]":authorHost, "friend[url]":authorUrl}
    #     request = self.factory.post('/api/friendrequest/', request_dict)
    #     response = friend_request(request)
    #     # check that it was accepted and status indicates refresh page required (because now friends)
    #     found = Friend.objects.filter(Q(requester_id=authorId,accepter_id=friendId, accepted=True) |
    #                                   Q(requester_id=friendId,accepter_id=authorId, accepted=True)).first()
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsNotNone(found)

    # def test_autofollow_complete_friendrequest(self):
    #     ''' make a duplicate friend request '''

    #     authorId = self.user_profile.guid
    #     authorName = self.user_profile.display_name
    #     friendId = self.user_profile2.guid
    #     friendName = self.user_profile2.display_name

    #     # self.user_profile.host = "http://127.0.0.1:8000/"
    #     authorHost = self.user_profile.host
    #     friendHost = self.user_profile2.host
    #     # user_profile doesn't have a url...
    #     authorUrl = "http://localhost:8000/author/"
    #     friendUrl = "http://localhost:8000/author/"+friendId

    #     request_dict = {"author[id]":authorId,"author[displayname]":authorName, "author[host]":authorHost, "author[url]":authorUrl,
    #                    "friend[id]":friendId,"friend[displayname]":friendName, "friend[host]":friendHost, "friend[url]":friendUrl}
    #     request = self.factory.post('/api/friendrequest/', request_dict)

    #     # make sure no one is already following
    #     follower = Follow.objects.filter(Q(follower_id=authorId, following_id=friendId)).first()
    #     following = Follow.objects.filter(Q(follower_id=friendId, following_id=authorId)).first()
    #     self.assertIsNone(follower)
    #     self.assertIsNone(following)

    #     # check that author is not following friend
    #     response = friend_request(request)
    #     follower = Follow.objects.filter(Q(follower_id=authorId, following_id=friendId)).first()
    #     following = Follow.objects.filter(Q(follower_id=friendId, following_id=authorId)).first()
    #     self.assertIsNotNone(follower)
    #     self.assertIsNone(following)
    #     self.assertEqual(response.status_code, 200)

    #     request_dict = {"author[id]":friendId,"author[displayname]":friendName, "author[host]":friendHost, "author[url]":friendUrl,
    #                    "friend[id]":authorId,"friend[displayname]":authorName, "friend[host]":authorHost, "friend[url]":authorUrl}
    #     request = self.factory.post('/api/friendrequest/', request_dict)
    #     response = friend_request(request)

    #     # check that friend is now following author
    #     follower = Follow.objects.filter(Q(follower_id=friendId, following_id=authorId)).first()
    #     following = Follow.objects.filter(Q(follower_id=authorId, following_id=friendId)).first()
    #     self.assertIsNotNone(follower)
    #     self.assertIsNotNone(following)
    #     self.assertEqual(response.status_code, 200)

    # def test_self_friendrequest(self):
    #     ''' try to make a friend request '''

    #     authorId = self.user_profile2.guid
    #     authorName = self.user_profile.display_name
    #     # self.user_profile.host = "http://127.0.0.1:8000/"
    #     authorHost = self.user_profile.host
    #     # user_profile doesn't have a url...
    #     authorUrl = "http://localhost:8000/author/"

    #     request_dict = {"author[id]":authorId,"author[displayname]":authorName, "author[host]":authorHost, "author[url]":authorUrl,
    #                    "friend[id]":authorId,"friend[displayname]":authorName, "friend[host]":authorHost, "friend[url]":authorUrl}
    #     request = self.factory.post('/api/friendrequest/', request_dict)

    #     response = friend_request(request)
    #     found = Friend.objects.filter(Q(requester_id=authorId,accepter_id=authorId)).first()
    #     self.assertEqual(response.status_code, 400)
    #     self.assertIsNone(found)

    # def test_invalid_authorId_friendrequest(self):
    #     ''' invalid author ID '''

    #     authorId = "INVALID ID"
    #     authorName = self.user_profile.display_name
    #     friendId = self.user_profile2.guid
    #     friendName = self.user_profile2.display_name

    #     # self.user_profile.host = "http://127.0.0.1:8000/"
    #     authorHost = self.user_profile.host
    #     friendHost = self.user_profile2.host
    #     # user_profile doesn't have a url...
    #     authorUrl = "http://localhost:8000/author/"
    #     friendUrl = "http://localhost:8000/author/"+friendId

    #     request_dict = {"author[id]":authorId,"author[displayname]":authorName, "author[host]":authorHost, "author[url]":authorUrl,
    #                    "friend[id]":friendId,"friend[displayname]":friendName, "friend[host]":friendHost, "friend[url]":friendUrl}
    #     request = self.factory.post('/api/friendrequest/', request_dict)

    #     # make sure it doesn't already exist
    #     found = Friend.objects.filter(requester_id=authorId).first()
    #     self.assertIsNone(found)

    #     response = friend_request(request)
    #     found = Friend.objects.filter(Q(requester_id=authorId,accepter_id=friendId) | Q(requester_id=friendId,accepter_id=authorId)).first()
    #     self.assertEqual(response.status_code,400)
    #     self.assertIsNotNone(found)

    # def test_invalid_authorName_friendrequest(self):
    #     ''' invalid author name (is GUID) '''

    #     authorId = self.user_profile.guid
    #     authorName = self.user_profile.guid
    #     friendId = self.user_profile2.guid
    #     friendName = self.user_profile2.display_name

    #     # self.user_profile.host = "http://127.0.0.1:8000/"
    #     authorHost = self.user_profile.host
    #     friendHost = self.user_profile2.host
    #     # user_profile doesn't have a url...
    #     authorUrl = "http://localhost:8000/author/"
    #     friendUrl = "http://localhost:8000/author/"+friendId

    #     request_dict = {"author[id]":authorId,"author[displayname]":authorName, "author[host]":authorHost, "author[url]":authorUrl,
    #                    "friend[id]":friendId,"friend[displayname]":friendName, "friend[host]":friendHost, "friend[url]":friendUrl}
    #     request = self.factory.post('/api/friendrequest/', request_dict)

    #     # make sure it doesn't already exist
    #     found = Friend.objects.filter(requester_id=authorId).first()
    #     self.assertIsNone(found)

    #     response = friend_request(request)
    #     found = Friend.objects.filter(Q(requester_id=authorId,accepter_id=friendId) | Q(requester_id=friendId,accepter_id=authorId)).first()
    #     self.assertEqual(response.status_code,400)
    #     self.assertIsNotNone(found)

    # def test_invalid_friendId_friendrequest(self):
    #     ''' invalid friend ID '''

    #     authorId = self.user_profile.guid
    #     authorName = self.user_profile.display_name
    #     friendId = "NOT A GUID"
    #     friendName = self.user_profile2.display_name

    #     # self.user_profile.host = "http://127.0.0.1:8000/"
    #     authorHost = self.user_profile.host
    #     friendHost = self.user_profile2.host
    #     # user_profile doesn't have a url...
    #     authorUrl = "http://localhost:8000/author/"
    #     friendUrl = "http://localhost:8000/author/"+friendId

    #     request_dict = {"author[id]":authorId,"author[displayname]":authorName, "author[host]":authorHost, "author[url]":authorUrl,
    #                    "friend[id]":friendId,"friend[displayname]":friendName, "friend[host]":friendHost, "friend[url]":friendUrl}
    #     request = self.factory.post('/api/friendrequest/', request_dict)

    #     # make sure it doesn't already exist
    #     found = Friend.objects.filter(requester_id=authorId).first()
    #     self.assertIsNone(found)

    #     response = friend_request(request)
    #     found = Friend.objects.filter(Q(requester_id=authorId,accepter_id=friendId) | Q(requester_id=friendId,accepter_id=authorId)).first()
    #     self.assertEqual(response.status_code,400)
    #     self.assertIsNotNone(found)

    # def test_empty_friendName_friendrequest(self):
    #     ''' empty friend name '''

    #     authorId = self.user_profile.guid
    #     authorName = self.user_profile.display_name
    #     friendId = self.user_profile2.guid
    #     friendName = ""

    #     # self.user_profile.host = "http://127.0.0.1:8000/"
    #     authorHost = self.user_profile.host
    #     friendHost = self.user_profile2.host
    #     # user_profile doesn't have a url...
    #     authorUrl = "http://localhost:8000/author/"
    #     friendUrl = "http://localhost:8000/author/"+friendId

    #     request_dict = {"author[id]":authorId,"author[displayname]":authorName, "author[host]":authorHost, "author[url]":authorUrl,
    #                    "friend[id]":friendId,"friend[displayname]":friendName, "friend[host]":friendHost, "friend[url]":friendUrl}
    #     request = self.factory.post('/api/friendrequest/', request_dict)

    #     # make sure it doesn't already exist
    #     found = Friend.objects.filter(requester_id=authorId).first()
    #     self.assertIsNone(found)

    #     response = friend_request(request)
    #     found = Friend.objects.filter(Q(requester_id=authorId,accepter_id=friendId) | Q(requester_id=friendId,accepter_id=authorId)).first()
    #     self.assertEqual(response.status_code,400)
    #     self.assertIsNotNone(found)

    def test_missing_friendName_friendrequest(self):
        ''' missing field '''

        authorId = self.user_profile.guid
        authorName = self.user_profile.display_name
        friendId = self.user_profile2.guid
        friendName = self.user_profile2.display_name

        # self.user_profile.host = "http://127.0.0.1:8000/"
        authorHost = self.user_profile.host
        friendHost = self.user_profile2.host
        # user_profile doesn't have a url...
        authorUrl = "http://localhost:8000/author/"
        friendUrl = "http://localhost:8000/author/"+friendId

        '''missing: "author[id]":authorId,'''
        request_dict = {"author[displayname]":authorName, "author[host]":authorHost, "author[url]":authorUrl,
                       "friend[id]":friendId,"friend[displayname]":friendName, "friend[host]":friendHost, "friend[url]":friendUrl}
        request = self.factory.post('/api/friendrequest/', request_dict)

        response = friend_request(request)
        found = Friend.objects.filter(Q(requester_id=authorId,accepter_id=friendId) | Q(requester_id=friendId,accepter_id=authorId)).first()
        self.assertEqual(response.status_code,400)
        self.assertIsNotNone(found)

    def test_not_implemented_paths(self):
        ''' Test all paths not implemented for error code 501 '''

        # # Factory for get request
        # request = self.factory.get('/api/friendrequest')
        #
        # response = friend_request(request)
        # self.assertEqual(response.status_code,501)
        #
        # # Factory for get request
        # request = self.factory.get('/api/friends/{}'.format(self.user_profile.guid))
        #
        # response = get_friends(request)
        # self.assertEqual(response.status_code,501)
        #
        # # Factory for get request
        # request = self.factory.get('/api/friends/{}/{}'.format(self.user_profile.guid, self.user_profile2.guid))
        #
        # response = is_friend(request)
        # self.assertEqual(response.status_code,501)

