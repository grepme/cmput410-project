from django.db import models
import urllib2, base64
import json

# import all of the models from each app
from comments.models import Comment
from friends.models import Friend, Follow
from posts.models import Post
from tags.models import Tag
from django.contrib.auth.models import User


class Server(models.Model):
    # localhost:8000/api
    host = models.CharField(max_length=50,primary_key=True)
    user_header = models.CharField(max_length=40)
    auth_type = models.CharField(max_length=6)
    auth_user = models.CharField(max_length=50)
    auth_password = models.CharField(max_length=50)
    realm = models.CharField(max_length=50)

    author_posts = models.CharField(max_length=60,default="/author/posts")
    author_id_posts = models.CharField(max_length=60,default="/author/{author_guid}/posts")
    posts = models.CharField(max_length=60,default="/posts")
    posts_id = models.CharField(max_length=60,default="/posts/{post_guid}")
    friends_id_id = models.CharField(max_length=60,default="/friends/{friend_guid}/{friend_2_guid}")
    friends_list = models.CharField(max_length=60,default="/friends/{friend_guid}")
    friend_request = models.CharField(max_length=60,default="/friendrequest")

    def post_friend_request(self,requester,accepter):

        request = urllib2.Request("{host}{path}".format(host=self.host,path=self.friend_request),
                json.dumps({"query":"friendrequest","author":requester.as_dict(), "friend":accepter.as_dict()}))
        # Assume basic Auth
        base64string = base64.encodestring('%s:%s' % (self.auth_user, self.auth_password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)

        try:
            result = urllib2.urlopen(request)
        except (urllib2.HTTPError, urllib2.URLError) as e:
            return e.code

        return None


    def get_posts(self):

        request = urllib2.Request("http://{host}{path}".format(host=self.host,path=self.posts))
        # Assume basic Auth
        base64string = base64.encodestring('%s:%s' % (self.auth_user, self.auth_password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        try:
            result = urllib2.urlopen(request)
        except (urllib2.HTTPError, urllib2.URLError) as e:
            print e.reason
            return e.code

        return result.read()

    def get_posts_id(self,post_guid):

        print "http://{host}{path}".format(host=self.host,path=self.posts).format(post_guid=post_guid)
        request = urllib2.Request("http://{host}{path}".format(host=self.host,path=self.posts).format(post_guid=post_guid))
        # Assume basic Auth
        base64string = base64.encodestring('%s:%s' % (self.auth_user, self.auth_password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        try:
            result = urllib2.urlopen(request)
        except (urllib2.HTTPError, urllib2.URLError) as e:
            print e.reason
            return e.code

        return result.read()

    def get_friends_id_id(self,friend_guid,friend_2_guid):

        request = urllib2.Request("http://{host}{path}".format(host=self.host,path=self.friends_id_id).format(friend_guid=friend_guid,friend_2_guid=friend_2_guid))
        # Assume basic Auth
        base64string = base64.encodestring('%s:%s' % (self.auth_user, self.auth_password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        try:
            result = urllib2.urlopen(request)
        except (urllib2.HTTPError, urllib2.URLError) as e:
            print e.reason
            return e.code

        return result.read()

    def get_friends_list(self,friend_guid,friends_list):

        post_data = {
            "query":"friends",
            "author":friend_guid,
            "authors":friends_list
            }

        path = "http://{host}{path}".format(host=self.host,path=self.friends_list).format(friend_guid=friend_guid)
        print path
        request = urllib2.Request(path,json.dumps(post_data))
        # Assume basic Auth
        base64string = base64.encodestring('%s:%s' % (self.auth_user, self.auth_password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        try:
            result = urllib2.urlopen(request)
        except (urllib2.HTTPError, urllib2.URLError) as e:
            print e.reason
            return e.code

        return result.read()


    def __unicode__(self):
        return self.text[:10]



