from django.contrib.auth.models import AnonymousUser, User
from django.db.models import Q
from django.db import transaction
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

    # def test_author_posts(self):
    #     ''' get the current logged in users visible posts '''

    #     # Factory for get request
    #     request = self.factory.get('/api/author/posts')

    #     # Set the user
    #     request.user = self.user;
    #     request.profile = self.user_profile;

    #     response = get_posts(request)
    #     json_obj = json.loads(response.content)
    #     self.assertEqual(json_obj['posts'],[])

    # def test_methods_author_posts(self):
    #     ''' make sure we cant wrong methods '''

    #     # Factory for get request
    #     request = self.factory.post('/api/author/posts')
    #     request.user = self.user;
    #     request.profile = self.user_profile;
    #     response = get_posts(request)
    #     self.assertEqual(response.status_code,405)

    #     request = self.factory.delete('/api/author/posts')
    #     request.user = self.user;
    #     request.profile = self.user_profile;
    #     response = get_posts(request)
    #     self.assertEqual(response.status_code,405)

    #     request = self.factory.put('/api/author/posts')
    #     request.user = self.user;
    #     request.profile = self.user_profile;
    #     response = get_posts(request)
    #     self.assertEqual(response.status_code,405)


    # def test_author_posts_id_incorrect(self):
    #     ''' get the current logged in users visible posts '''

    #     Post.objects.create(title='randomtitle', date=timezone.now(), text='sometext', image=None,
    #                              visibility=Post.friend, commonmark=False, author=self.user_profile, origin="localhost", source="localhost")

    #     # Factory for get request
    #     request = self.factory.get('/api/author/{}/posts'.format(self.user2.id))

    #     # Set the user
    #     request.user = self.user;
    #     request.profile = self.user_profile;

    #     response = get_posts(request,self.user_profile2.guid)
    #     json_obj = json.loads(response.content)
    #     self.assertEqual(json_obj['posts'],[])

    # def test_author_posts_id_correct(self):
    #     ''' get specific authors posts '''

    #     Post.objects.create(title='randomtitle', date=timezone.now(), text='sometext', image=None,
    #                              visibility=Post.friend, commonmark=False, author=self.user_profile, origin="localhost", source="localhost")

    #     # Factory for get request
    #     request = self.factory.get('/api/author/{}/posts'.format(self.user_profile.guid))

    #     # Set the user
    #     request.user = self.user;
    #     request.profile = self.user_profile;

    #     response = get_posts(request,self.user_profile.guid)
    #     json_obj = json.loads(response.content)
    #     self.assertEqual(len(json_obj['posts']),1)

    # def test_author_posts_id_not_self(self):
    #     ''' get another users posts'''

    #     Post.objects.create(title='randomtitlepublic', date=timezone.now(), text='sometext', image=None,
    #                              visibility=Post.public, commonmark=False, author=self.user_profile2, origin="localhost", source="localhost")

    #     Post.objects.create(title='randomtitle', date=timezone.now(), text='sometext', image=None,
    #                              visibility=Post.friend, commonmark=False, author=self.user_profile2, origin="localhost", source="localhost")
    #     Post.objects.create(title='randomtitle', date=timezone.now(), text='sometext', image=None,
    #                              visibility=Post.private, commonmark=False, author=self.user_profile2, origin="localhost", source="localhost")
    #     Post.objects.create(title='randomtitle', date=timezone.now(), text='sometext', image=None,
    #                              visibility=Post.FOAF, commonmark=False, author=self.user_profile2, origin="localhost", source="localhost")

    #     # Factory for get request
    #     request = self.factory.get('/api/author/{}/posts'.format(self.user_profile2.guid))

    #     # Set the user
    #     request.user = self.user;
    #     request.profile = self.user_profile;

    #     response = get_posts(request,self.user_profile2.guid)
    #     json_obj = json.loads(response.content)
    #     self.assertEqual(len(json_obj['posts']),1)
    #     self.assertEqual(json_obj['posts'][0]['title'],'randomtitlepublic')

    # def test_author_posts_id_doesnot_exist(self):
    #     ''' try to get a invalid users posts'''

    #     author_id = 20000

    #     Post.objects.create(title='randomtitlepublic', date=timezone.now(), text='sometext', image=None,
    #                              visibility=Post.public, commonmark=False, author=self.user_profile2, origin="localhost", source="localhost")

    #     Post.objects.create(title='randomtitle', date=timezone.now(), text='sometext', image=None,
    #                              visibility=Post.friend, commonmark=False, author=self.user_profile2, origin="localhost", source="localhost")
    #     Post.objects.create(title='randomtitle', date=timezone.now(), text='sometext', image=None,
    #                              visibility=Post.private, commonmark=False, author=self.user_profile2, origin="localhost", source="localhost")
    #     Post.objects.create(title='randomtitle', date=timezone.now(), text='sometext', image=None,
    #                              visibility=Post.FOAF, commonmark=False, author=self.user_profile2, origin="localhost", source="localhost")

    #     # Factory for get request
    #     request = self.factory.get('/api/author/{}/posts'.format(author_id))

    #     # Set the user
    #     request.user = self.user;
    #     request.profile = self.user_profile;

    #     response = get_posts(request,author_id)
    #     json_obj = json.loads(response.content)
    #     self.assertEqual(response.status_code,404)
    #     self.assertEqual(json_obj['message'],"Author with id {} does not exist".format(author_id))

    # def test_invalid_accept(self):
    #     ''' try to get with invalid accept '''

    #     # Factory for get request
    #     request = self.factory.get('/api/author/%s/posts' % self.user_profile2.guid,Accept='html/text')

    #     # Set the user
    #     request.user = self.user;
    #     request.profile = self.user_profile;

    #     response = get_posts(request,self.user_profile2.guid)
    #     self.assertEqual(response.status_code,406)


    # def test_invalid_accept_2(self):
    #     ''' try to get with invalid accept '''

    #     # Factory for get request
    #     request = self.factory.get('/api/author/posts',Accept='html/text')

    #     # Set the user
    #     request.user = self.user;
    #     request.profile = self.user_profile;

    #     response = get_posts(request)
    #     self.assertEqual(response.status_code,406)

    # def test_invalid_accept_api_posts(self):
    #     ''' try to get with invalid accept /api/posts'''

    #     # Factory for get request
    #     request = self.factory.get('/api/posts',Accept='html/text')

    #     # Set the user
    #     request.user = self.user;
    #     request.profile = self.user_profile;
    #     response = get_post(request)
    #     self.assertEqual(response.status_code,406)

    # def test_invalid_accept_api_posts_id(self):
    #     post_id = uuid.uuid1().__str__()
    #     ''' try to get with invalid accept /api/posts/200'''

    #     # Factory for get request
    #     request = self.factory.get('/api/posts/{}'.format(post_id,Accept='html/text'))

    #     # Set the user
    #     request.user = self.user
    #     request.profile = self.user_profile
    #     response = get_post(request,post_id)
    #     print response
    #     self.assertEqual(response.status_code,406)


    # def test_methods_posts(self):
    #     ''' make sure we cant wrong methods '''

    #     # Factory for get request
    #     request = self.factory.post('/api/posts')
    #     request.user = self.user;
    #     request.profile = self.user_profile;
    #     response = get_posts(request)
    #     self.assertEqual(response.status_code,405)

    #     request = self.factory.delete('/api/posts')
    #     request.user = self.user;
    #     request.profile = self.user_profile;
    #     response = get_posts(request)
    #     self.assertEqual(response.status_code,405)

    #     request = self.factory.put('/api/posts')
    #     request.user = self.user;
    #     request.profile = self.user_profile;
    #     response = get_posts(request)
    #     self.assertEqual(response.status_code,405)

    # def test_post_id_doesnot_exist(self):
    #     ''' try to get a invalid post'''

    #     post_id = uuid.uuid1().__str__()

    #     Post.objects.create(title='randomtitlepublic', date=timezone.now(), text='sometext', image=None,
    #                              visibility=Post.public, commonmark=False, author=self.user_profile2, origin="localhost", source="localhost")

    #     # Factory for get request
    #     request = self.factory.get('/api/posts/%s/' % post_id )

    #     # Set the user
    #     request.user = self.user;
    #     request.profile = self.user_profile;

    #     response = get_post(request,post_id)
    #     json_obj = json.loads(response.content)
    #     self.assertEqual(response.status_code,404)
    #     self.assertEqual(json_obj['message'],"Post with id {} does not exist".format(post_id))

    # def test_post_id_exist(self):
    #     ''' try to get a post'''

    #     post = Post.objects.create(title='randomtitlepublic', date=timezone.now(), text='sometext', image=None,
    #                              visibility=Post.public, commonmark=False, author=self.user_profile2, origin="localhost", source="localhost")

    #     # Factory for get request
    #     request = self.factory.get('/api/posts/{}/'.format(post.guid))

    #     # Set the user
    #     request.user = self.user;
    #     request.profile = self.user_profile;

    #     response = get_post(request,post.guid)
    #     json_obj = json.loads(response.content)
    #     self.assertEqual(response.status_code,200)
    #     self.assertEqual(len(json_obj['posts']),1)

    # def test_send_friendrequest(self):
    #     ''' try to make a friend request '''

    #     newUser = User.objects.create_user(
    #         username='one', email='one@email.com', password='one')
    #     newProfile = Profile.objects.create(author=newUser, display_name="One")
    #     secondUser = User.objects.create_user(
    #         username='two', email='two@email.com', password='two')
    #     secondProfile = Profile.objects.create(author=secondUser, display_name="two")

    #     request_dict = json.dumps({"author":newProfile.as_dict(), "friend":secondProfile.as_dict()})
    #     request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')

    #     # make sure it doesn't already exist
    #     found = Friend.objects.filter(requester=newProfile).first()
    #     self.assertIsNone(found)

    #     response = friend_request(request)
    #     found = Friend.objects.filter(Q(requester=newProfile,
    #                                   accepter=secondProfile)).first()
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsNotNone(found)

    # def test_autofollow_friendrequest(self):
    #     ''' ensure friend request autofollows '''

    #     newUser = User.objects.create_user(
    #         username='three', email='three@email.com', password='three')
    #     newProfile = Profile.objects.create(author=newUser, display_name="three")
    #     secondUser = User.objects.create_user(
    #         username='four', email='four@email.com', password='four')
    #     secondProfile = Profile.objects.create(author=secondUser, display_name="four")

    #     request_dict = json.dumps({"author":newProfile.as_dict(), "friend":secondProfile.as_dict()})
    #     request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')

    #     # make sure it doesn't already exist
    #     follower = Follow.objects.filter(Q(follower=newProfile, following=secondProfile)).first()
    #     self.assertIsNone(follower)
    #     with transaction.atomic():
    #         response = friend_request(request)
    #     follower = Follow.objects.filter(Q(follower=newProfile, following=secondProfile)).first()
    #     self.assertEqual(response.status_code,200)
    #     self.assertIsNotNone(follower)

    # def test_send_duplicate_friendrequest(self):
    #     ''' make a duplicate friend request '''

    #     newUser = User.objects.create_user(
    #         username='five', email='five@email.com', password='five')
    #     newProfile = Profile.objects.create(author=newUser, display_name="five")
    #     secondUser = User.objects.create_user(
    #         username='six', email='six@email.com', password='six')
    #     secondProfile = Profile.objects.create(author=secondUser, display_name="six")

    #     request_dict = json.dumps({"author":newProfile.as_dict(), "friend":secondProfile.as_dict()})
    #     request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')

    #     # make sure it doesn't already exist
    #     found = Friend.objects.filter(requester=newProfile).first()
    #     self.assertIsNone(found)
    #     with transaction.atomic():
    #         response = friend_request(request)
    #     with transaction.atomic():
    #         response = friend_request(request)
    #     # check that duplicate didn't accept wrongfully
    #     found = Friend.objects.filter(Q(requester=newProfile,accepter=secondProfile, accepted=False) |
    #                                   Q(requester=secondProfile,accepter=newProfile, accepted=False)).first()
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsNotNone(found)

    # def test_complete_friendrequest(self):
    #     ''' complete friend request '''

    #     newUser = User.objects.create_user(
    #         username='seven', email='seven@email.com', password='seven')
    #     newProfile = Profile.objects.create(author=newUser, display_name="seven")
    #     secondUser = User.objects.create_user(
    #         username='eight', email='eight@email.com', password='eight')
    #     secondProfile = Profile.objects.create(author=secondUser, display_name="eight")

    #     request_dict = json.dumps({"author":newProfile.as_dict(), "friend":secondProfile.as_dict()})
    #     request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')

    #     # make sure it is not already accepted
    #     found = Friend.objects.filter(Q(requester=newProfile,accepter=secondProfile, accepted=True) |
    #                                   Q(requester=secondProfile,accepter=newProfile, accepted=True)).first()

    #     response = friend_request(request)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsNone(found)

    #     request_dict = json.dumps({"author":secondProfile.as_dict(), "friend":newProfile.as_dict()})
    #     request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')

    #     response = friend_request(request)

    #     # check that it was accepted and status indicates refresh page required (because now friends)
    #     found = Friend.objects.filter(Q(requester=newProfile,accepter=secondProfile, accepted=True) |
    #                                   Q(requester=secondProfile,accepter=newProfile, accepted=True)).first()
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsNotNone(found)

    # def test_autofollow_complete_friendrequest(self):
    #     ''' test autofollow on friend request '''

    #     newUser = User.objects.create_user(
    #         username='nine', email='nine@email.com', password='nine')
    #     newProfile = Profile.objects.create(author=newUser, display_name="nine")
    #     secondUser = User.objects.create_user(
    #         username='ten', email='ten@email.com', password='ten')
    #     secondProfile = Profile.objects.create(author=secondUser, display_name="ten")

    #     request_dict = json.dumps({"author":newProfile.as_dict(), "friend":secondProfile.as_dict()})
    #     request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')

    #     # make sure no one is already following
    #     follower = Follow.objects.filter(Q(follower=newProfile, following=secondProfile)).first()
    #     following = Follow.objects.filter(Q(follower=secondProfile, following_id=newProfile)).first()
    #     self.assertIsNone(follower)
    #     self.assertIsNone(following)

    #     # check that author is not following friend
    #     response = friend_request(request)

    #     follower = Follow.objects.filter(Q(follower=newProfile, following=secondProfile)).first()
    #     following = Follow.objects.filter(Q(follower=secondProfile, following=newProfile)).first()
    #     self.assertIsNotNone(follower)
    #     self.assertIsNone(following)
    #     self.assertEqual(response.status_code, 200)

    #     request_dict = json.dumps({"author":secondProfile.as_dict(), "friend":newProfile.as_dict()})
    #     request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')
    #     response = friend_request(request)

    #     # check that friend is now following author
    #     follower = Follow.objects.filter(Q(follower=secondProfile, following=newProfile)).first()
    #     following = Follow.objects.filter(Q(follower=newProfile, following=secondProfile)).first()
    #     self.assertIsNotNone(follower)
    #     self.assertIsNotNone(following)
    #     self.assertEqual(response.status_code, 200)

    # def test_self_friendrequest(self):
    #     ''' try to make a friend request '''
    #     newUser = User.objects.create_user(
    #         username='11', email='11@email.com', password='11')
    #     newProfile = Profile.objects.create(author=newUser, display_name="11")
    #     secondUser = User.objects.create_user(
    #         username='12', email='12@email.com', password='12')
    #     secondProfile = Profile.objects.create(author=secondUser, display_name="12")

    #     request_dict = json.dumps({"author":newProfile.as_dict(), "friend":newProfile.as_dict()})
    #     request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')

    #     response = friend_request(request)
    #     found = Friend.objects.filter(Q(requester=newProfile,accepter=newProfile)).first()
    #     self.assertEqual(response.status_code, 400)
    #     self.assertIsNone(found)


    # def test_empty_displayName_friendrequest(self):
    #     ''' invalid author name (is GUID) '''

    #     newUser = User.objects.create_user(
    #         username='newUser', email='13@email.com', password='13')
    #     newProfile = Profile.objects.create(author=newUser, display_name="")
    #     secondUser = User.objects.create_user(
    #         username='15', email='15@email.com', password='15')
    #     secondProfile = Profile.objects.create(author=secondUser, display_name="15")

    #     request_dict = json.dumps({"author":newProfile.as_dict(), "friend":secondProfile.as_dict()})
    #     request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')

    #     response = friend_request(request)
    #     found = Friend.objects.filter(Q(requester=newProfile,accepter=secondProfile)).first()
    #     self.assertEqual(response.status_code, 400)
    #     self.assertIsNotNone(found)

    # def test_already_following_friendrequest(self):
    #     ''' test that there exists only one Follow when friending someone followed '''

    #     newUser = User.objects.create_user(
    #         username='888', email='888@email.com', password='888')
    #     newProfile = Profile.objects.create(author=newUser, display_name="888")
    #     secondUser = User.objects.create_user(
    #         username='999', email='999@email.com', password='999')
    #     secondProfile = Profile.objects.create(author=secondUser, display_name="999")

    #     Follow.objects.create(follower=newProfile,following=secondProfile)
    #     firstFound = Follow.objects.filter(Q(follower=newProfile,following=secondProfile))

    #     request_dict = json.dumps({"author":newProfile.as_dict(), "friend":secondProfile.as_dict()})
    #     request = self.factory.post('/api/friendrequest/', data=request_dict, content_type='application/json')

    #     response = friend_request(request)

    #     found = Follow.objects.filter(Q(follower=newProfile,following=secondProfile))
    #     self.assertIsNotNone(found)
    #     self.assertEquals(response.status_code,200)
    #     #TODO: Make sure these are the same found FOLLOW objects?
    #     # self.assertEquals(firstFound, found)

    def test_valid_getfriends(self):
        ''' test get all friends of a list with only friends '''

        firstUser = User.objects.create_user(
            username='a1', email='a1@email.com', password='a1')
        firstProfile = Profile.objects.create(author=firstUser, display_name="a1")
        secondUser = User.objects.create_user(
            username='a2', email='a2@email.com', password='a2')
        secondProfile = Profile.objects.create(author=secondUser, display_name="a2")
        thirdUser = User.objects.create_user(
            username='a3', email='a3@email.com', password='a3')
        thirdProfile = Profile.objects.create(author=thirdUser, display_name="a3")

        Friend.objects.create(requester=secondProfile,accepter=firstProfile)
        Friend.objects.create(requester=thirdProfile,accepter=firstProfile)
        firstFound = Friend.objects.filter(Q(accepter=firstProfile,requester=secondProfile))
        secondFound = Friend.objects.filter(Q(accepter=firstProfile,requester=thirdProfile))
        self.assertIsNotNone(firstFound)
        self.assertIsNotNone(secondFound)

        authors = list()
        authors.append(secondProfile.as_dict())
        authors.append(thirdProfile.as_dict())
        request_dict = json.dumps({"author":firstProfile.as_dict(), "authors":authors})

        request = self.factory.post('/api/friends/'+str(firstProfile.guid), data=request_dict, content_type='application/json')
        response = get_friends(request,author_id=firstProfile.guid)
        print(response)

        # found = Follow.objects.filter(Q(follower=firstProfile,following=secondProfile))
        # self.assertIsNotNone(found)
        # self.assertEquals(response.status_code,200)
        #TODO: Make sure these are the same found FOLLOW objects?
        # self.assertEquals(firstFound, found)


    # def test_not_implemented_paths(self):
    #     ''' Test all paths not implemented for error code 501 '''

    #     # Factory for get request
    #     request = self.factory.get('/api/friendrequest')

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




