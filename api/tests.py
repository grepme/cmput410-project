from django.contrib.auth.models import AnonymousUser, User
from django.db import transaction
from django.db.models import Q
from posts.models import Post
from friends.models import Friend, Follow
from user_profile.models import Profile
from django.test import TestCase, RequestFactory
from django.utils import timezone
from api.models import Server
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

    def test_send_friendrequest(self):
        ''' try to make a friend request '''

        newUser = User.objects.create_user(
            username='one', email='one@email.com', password='one')
        newProfile = Profile.objects.create(author=newUser, display_name="One")
        secondUser = User.objects.create_user(
            username='two', email='two@email.com', password='two')
        secondProfile = Profile.objects.create(author=secondUser, display_name="two")

        request_dict = json.dumps({"author":newProfile.as_dict(), "friend":secondProfile.as_dict()})
        request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')

        # make sure it doesn't already exist
        found = Friend.objects.filter(requester_id=newProfile.guid).first()
        self.assertIsNone(found)

        response = friend_request(request)
        found = Friend.objects.filter(Q(requester_id=newProfile.guid,
                                      accepter_id=secondProfile.guid)).first()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(found)

    def test_autofollow_friendrequest(self):
        ''' ensure friend request autofollows '''

        newUser = User.objects.create_user(
            username='three', email='three@email.com', password='three')
        newProfile = Profile.objects.create(author=newUser, display_name="three")
        secondUser = User.objects.create_user(
            username='four', email='four@email.com', password='four')
        secondProfile = Profile.objects.create(author=secondUser, display_name="four")

        request_dict = json.dumps({"author":newProfile.as_dict(), "friend":secondProfile.as_dict()})
        request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')

        # make sure it doesn't already exist
        follower = Follow.objects.filter(Q(follower_id=newProfile.guid, following_id=secondProfile.guid)).first()
        self.assertIsNone(follower)

        response = friend_request(request)
        follower = Follow.objects.filter(Q(follower_id=newProfile.guid, following_id=secondProfile.guid)).first()
        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(follower)
    # TODO: Uncomment
    # def test_send_duplicate_friendrequest(self):
    #     ''' make a duplicate friend request '''
    #
    #     newUser = User.objects.create_user(
    #         username='five', email='five@email.com', password='five')
    #     newProfile = Profile.objects.create(author=newUser, display_name="five")
    #     secondUser = User.objects.create_user(
    #         username='six', email='six@email.com', password='six')
    #     secondProfile = Profile.objects.create(author=secondUser, display_name="six")
    #
    #     request_dict = json.dumps({"author":newProfile.as_dict(), "friend":secondProfile.as_dict()})
    #     request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')
    #
    #     # make sure it doesn't already exist
    #     found = Friend.objects.filter(requester_id=newProfile.guid).first()
    #     self.assertIsNone(found)
    #
    #     response = friend_request(request)
    #     response = friend_request(request)
    #     # check that duplicate didn't accept wrongfully
    #     found = Friend.objects.filter(Q(requester_id=newProfile.guid,accepter_id=secondProfile.guid, accepted=False) |
    #                                   Q(requester_id=secondProfile.guid,accepter_id=newProfile.guid, accepted=False)).first()
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsNotNone(found, "Duplicate Friend was not found")

    # def test_send_multiple_friendrequest(self):
    #     ''' try to make a friend request '''
    #
    #     newUser = User.objects.create_user(
    #         username='GREG', email='GREG@email.com', password='GREG')
    #     newProfile = Profile.objects.create(author=newUser, display_name="GREG")
    #     secondUser = User.objects.create_user(
    #         username='TRACE', email='TRACE@email.com', password='TRACE')
    #     secondProfile = Profile.objects.create(author=secondUser, display_name="TRACE")
    #     thirdUser = User.objects.create_user(
    #         username='FRANKIE', email='FRANKIE@email.com', password='FRANKIE')
    #     thirdProfile = Profile.objects.create(author=thirdUser, display_name="FRANKIE")
    #
    #     request_dict = json.dumps({"author":newProfile.as_dict(), "friend":secondProfile.as_dict()})
    #     request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')
    #     with transaction.atomic():
    #         response = friend_request(request)
    #     found = Friend.objects.filter(Q(requester_id=newProfile.guid, accepter_id=secondProfile.guid)).first()
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsNotNone(found)
    #
    #     request_dict = json.dumps({"author":newProfile.as_dict(), "friend":thirdProfile.as_dict()})
    #     request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')
    #     with transaction.atomic():
    #         response = friend_request(request)
    #     # Make sure second friend request was a success
    #     found = Friend.objects.filter(Q(requester_id=newProfile.guid, accepter_id=thirdProfile.guid)).first()
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsNotNone(found, "Could not find second friend request")

    def test_complete_friendrequest(self):
        ''' complete friend request '''

        newUser = User.objects.create_user(
            username='seven', email='seven@email.com', password='seven')
        newProfile = Profile.objects.create(author=newUser, display_name="seven")
        secondUser = User.objects.create_user(
            username='eight', email='eight@email.com', password='eight')
        secondProfile = Profile.objects.create(author=secondUser, display_name="eight")

        request_dict = json.dumps({"author":newProfile.as_dict(), "friend":secondProfile.as_dict()})
        request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')

        # make sure it is not already accepted
        found = Friend.objects.filter(Q(requester_id=newProfile.guid,accepter_id=secondProfile.guid, accepted=True) |
                                      Q(requester_id=secondProfile.guid,accepter_id=newProfile.guid, accepted=True)).first()

        response = friend_request(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(found)

        request_dict = json.dumps({"author":secondProfile.as_dict(), "friend":newProfile.as_dict()})
        request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')

        response = friend_request(request)

        # check that it was accepted and status indicates refresh page required (because now friends)
        found = Friend.objects.filter(Q(requester_id=newProfile.guid,accepter_id=secondProfile.guid, accepted=True) |
                                      Q(requester_id=secondProfile.guid,accepter_id=newProfile.guid, accepted=True)).first()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(found)

    # def test_existing_friendrequest(self):
    #     ''' make request to existing friend '''
    #
    #     newUser = User.objects.create_user(
    #         username='purple', email='purple@email.com', password='purple')
    #     newProfile = Profile.objects.create(author=newUser, display_name="purple")
    #     secondUser = User.objects.create_user(
    #         username='blue', email='blue@email.com', password='blue')
    #     secondProfile = Profile.objects.create(author=secondUser, display_name="blue")
    #
    #     request_dict = json.dumps({"author":newProfile.as_dict(), "friend":secondProfile.as_dict()})
    #     request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')
    #
    #     # make sure it is not already accepted
    #     found = Friend.objects.filter(Q(requester_id=newProfile.guid,accepter_id=secondProfile.guid, accepted=True) |
    #                                   Q(requester_id=secondProfile.guid,accepter_id=newProfile.guid, accepted=True)).first()
    #     # send first request
    #     with transaction.atomic():
    #         response = friend_request(request)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsNone(found)
    #
    #     request_dict = json.dumps({"author":secondProfile.as_dict(), "friend":newProfile.as_dict()})
    #     request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')
    #     # send second request (accept first)
    #     with transaction.atomic():
    #         response = friend_request(request)
    #
    #     # check that it was accepted and status indicates refresh page required (because now friends)
    #     found = Friend.objects.filter(Q(requester_id=newProfile.guid,accepter_id=secondProfile.guid, accepted=True) |
    #                                   Q(requester_id=secondProfile.guid,accepter_id=newProfile.guid, accepted=True))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(len(found), 1)
    #     # send request although friendship already completed
    #     request_dict = json.dumps({"author":newProfile.as_dict(), "friend":secondProfile.as_dict()})
    #     request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')
    #     with transaction.atomic():
    #         response = friend_request(request)
    #
    #     # check that only 1 Friend object still exists
    #     found = Friend.objects.filter(Q(requester_id=newProfile.guid,accepter_id=secondProfile.guid, accepted=True) |
    #                                   Q(requester_id=secondProfile.guid,accepter_id=newProfile.guid, accepted=True))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(len(found), 1)

    def test_autofollow_complete_friendrequest(self):
        ''' test autofollow on friend request '''

        newUser = User.objects.create_user(
            username='nine', email='nine@email.com', password='nine')
        newProfile = Profile.objects.create(author=newUser, display_name="nine")
        secondUser = User.objects.create_user(
            username='ten', email='ten@email.com', password='ten')
        secondProfile = Profile.objects.create(author=secondUser, display_name="ten")

        request_dict = json.dumps({"author":newProfile.as_dict(), "friend":secondProfile.as_dict()})
        request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')

        # make sure no one is already following
        follower = Follow.objects.filter(Q(follower_id=newProfile.guid, following_id=secondProfile.guid)).first()
        following = Follow.objects.filter(Q(follower_id=secondProfile.guid, following_id=newProfile.guid)).first()
        self.assertIsNone(follower)
        self.assertIsNone(following)

        # check that author is not following friend
        response = friend_request(request)

        follower = Follow.objects.filter(Q(follower_id=newProfile.guid, following_id=secondProfile.guid)).first()
        following = Follow.objects.filter(Q(follower_id=secondProfile.guid, following_id=newProfile.guid)).first()
        self.assertIsNotNone(follower)
        self.assertIsNone(following)
        self.assertEqual(response.status_code, 200)

        request_dict = json.dumps({"author":secondProfile.as_dict(), "friend":newProfile.as_dict()})
        request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')
        response = friend_request(request)

        # check that friend is now following author
        follower = Follow.objects.filter(Q(follower_id=secondProfile.guid, following_id=newProfile.guid)).first()
        following = Follow.objects.filter(Q(follower_id=newProfile.guid, following_id=secondProfile.guid)).first()
        self.assertIsNotNone(follower)
        self.assertIsNotNone(following)
        self.assertEqual(response.status_code, 200)

    def test_self_friendrequest(self):
        ''' try to make a friend request '''
        newUser = User.objects.create_user(
            username='11', email='11@email.com', password='11')
        newProfile = Profile.objects.create(author=newUser, display_name="11")
        secondUser = User.objects.create_user(
            username='12', email='12@email.com', password='12')
        secondProfile = Profile.objects.create(author=secondUser, display_name="12")

        request_dict = json.dumps({"author":newProfile.as_dict(), "friend":newProfile.as_dict()})
        request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')

        response = friend_request(request)
        found = Friend.objects.filter(Q(requester_id=newProfile.as_dict(),accepter_id=newProfile.as_dict())).first()
        self.assertEqual(response.status_code, 400)
        self.assertIsNone(found)
    # TODO: Uncomment
    # def test_empty_name_friendrequest(self):
    #     ''' invalid author ID '''
    #
    #     newUser = User.objects.create_user(
    #         username='', email='13@email.com', password='13')
    #     newProfile = Profile.objects.create(author=newUser, display_name="123")
    #     secondUser = User.objects.create_user(
    #         username='14', email='14@email.com', password='14')
    #     secondProfile = Profile.objects.create(author=secondUser, display_name="14")
    #
    #     request_dict = json.dumps({"author":newProfile.as_dict(), "friend":secondProfile.as_dict()})
    #     request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')
    #
    #     response = friend_request(request)
    #     found = Friend.objects.filter(Q(requester_id=newProfile.as_dict(),accepter_id=secondProfile.as_dict())).first()
    #     self.assertEqual(response.status_code, 400)
    #     self.assertIsNotNone(found)
    # TODO: Uncomment
    # def test_empty_displayName_friendrequest(self):
    #     ''' invalid author name (is GUID) '''
    #
    #     newUser = User.objects.create_user(
    #         username='newUser', email='13@email.com', password='13')
    #     newProfile = Profile.objects.create(author=newUser, display_name="")
    #     secondUser = User.objects.create_user(
    #         username='15', email='15@email.com', password='15')
    #     secondProfile = Profile.objects.create(author=secondUser, display_name="15")
    #
    #     request_dict = json.dumps({"author":newProfile.as_dict(), "friend":secondProfile.as_dict()})
    #     request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')
    #
    #     response = friend_request(request)
    #     found = Friend.objects.filter(Q(requester_id=newProfile.as_dict(),accepter_id=secondProfile.as_dict())).first()
    #     self.assertEqual(response.status_code, 400)
    #     self.assertIsNotNone(found)

    # TODO: Test friend request of two other people?

    def test_already_following_friendrequest(self):
        ''' test that there exists only one Follow when friending someone followed '''

        newUser = User.objects.create_user(
            username='nine', email='nine@email.com', password='nine')
        newProfile = Profile.objects.create(author=newUser, display_name="nine")
        secondUser = User.objects.create_user(
            username='ten', email='ten@email.com', password='ten')
        secondProfile = Profile.objects.create(author=secondUser, display_name="ten")

        Follow.objects.create(follower=newProfile,following=secondProfile)
        firstFound = Follow.objects.filter(Q(follower=newProfile.guid,following=secondProfile.guid))

        request_dict = json.dumps({"author":newProfile.as_dict(), "friend":secondProfile.as_dict()})
        request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')

        response = friend_request(request)

        found = Follow.objects.filter(Q(follower=newProfile.guid,following=secondProfile.guid))
        self.assertEquals(response.status_code,200)
        #TODO: Make sure these are the same found FOLLOW objects?
        # self.assertEquals(firstFound, found)

    def test_get_single_friends(self):
        ''' test that there exists only one Follow when friending someone followed '''

        newUser = User.objects.create_user(
            username='bob', email='bob@email.com', password='bob')
        newProfile = Profile.objects.create(author=newUser, display_name="bob")
        secondUser = User.objects.create_user(
            username='jill', email='jill@email.com', password='jill')
        secondProfile = Profile.objects.create(author=secondUser, display_name="jill")

        request_dict = json.dumps({"author":newProfile.as_dict(), "friend":secondProfile.as_dict()})
        request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')
        response = friend_request(request)
        # make sure newProfile has friend reqeust to second Profile
        found = Follow.objects.filter(Q(follower=newProfile.guid,following=secondProfile.guid))
        self.assertIsNotNone(found)
        self.assertEquals(response.status_code,200)

        request_dict = json.dumps({"author":secondProfile.as_dict(), "friend":newProfile.as_dict()})
        request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')
        response = friend_request(request)
        # complete friend request
        found = Follow.objects.filter(Q(follower=secondProfile.guid,following=newProfile.guid))
        self.assertIsNotNone(found)
        self.assertEquals(response.status_code,200)

        request.profile = newProfile
        request_dict = json.dumps({"author":newProfile.guid, "authors":[secondProfile.guid]})
        request = self.factory.post('/api/friend/{}'.format(newProfile.guid), data=request_dict, content_type='application/json')
        response = get_friends(request, newProfile.guid)
        self.assertEquals(response.status_code, 200)

    def test_get_multiple_friends(self):
        ''' test that there exists only one Follow when friending someone followed '''

        newUser = User.objects.create_user(
            username='dane', email='dane@email.com', password='dane')
        newProfile = Profile.objects.create(author=newUser, display_name="dane")
        secondUser = User.objects.create_user(
            username='cook', email='cook@email.com', password='cook')
        secondProfile = Profile.objects.create(author=secondUser, display_name="cook")
        thirdUser = User.objects.create_user(
            username='gregory', email='gregory@email.com', password='gregory')
        thirdProfile = Profile.objects.create(author=thirdUser, display_name="gregory")

        request_dict = json.dumps({"author":newProfile.as_dict(), "friend":secondProfile.as_dict()})
        request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')
        with transaction.atomic():
            response = friend_request(request)
        # make sure newProfile has friend reqeust to second Profile
        found = Follow.objects.filter(Q(follower=newProfile.guid,following=secondProfile.guid))
        self.assertIsNotNone(found)
        self.assertEquals(response.status_code,200)

        request_dict = json.dumps({"author":newProfile.as_dict(), "friend":thirdProfile.as_dict()})
        request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')
        with transaction.atomic():
            response = friend_request(request)
        # make sure newProfile has friend reqeust to second Profile
        found = Follow.objects.filter(Q(follower=newProfile.guid,following=thirdProfile.guid))
        self.assertIsNotNone(found)
        self.assertEquals(response.status_code,200)

        request_dict = json.dumps({"author":secondProfile.as_dict(), "friend":newProfile.as_dict()})
        request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')
        with transaction.atomic():
            response = friend_request(request)
        # complete friend request
        found = Follow.objects.filter(Q(follower=secondProfile.guid,following=newProfile.guid))
        self.assertIsNotNone(found)
        self.assertEquals(response.status_code,200)

        request_dict = json.dumps({"author":thirdProfile.as_dict(), "friend":newProfile.as_dict()})
        request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')
        with transaction.atomic():
            response = friend_request(request)
        # make sure newProfile has friend reqeust to second Profile
        found = Follow.objects.filter(Q(follower=thirdProfile.guid,following=newProfile.guid))
        self.assertIsNotNone(found)
        self.assertEquals(response.status_code,200)

        request.profile = newProfile
        request_dict = json.dumps({"author":newProfile.guid, "authors":[secondProfile.guid, thirdProfile.guid]})
        request = self.factory.post('/api/friend/{}'.format(newProfile.guid), data=request_dict, content_type='application/json')
        with transaction.atomic():
            response = get_friends(request, newProfile.guid)
        self.assertEquals(response.status_code, 200)
        print("THIS IS NOT DONE. TEST LENGTH OF RETURNED LIST")
        self.assertFalse(True, "come back to me here")
        print(response)




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




