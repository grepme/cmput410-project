from django.db import models
from django.contrib.auth.models import User
from user_profile.models import Profile
# Create your models here.

class Follow(models.Model):
    # when started following
    date = models.DateTimeField(auto_now_add=True)
    # who started following
    follower = models.ForeignKey(Profile, related_name="follower",primary_key=True)
    # who was followed
    following = models.ForeignKey(Profile, related_name="following")

    def __unicode__(self):
        return u"{} -> {}".format(self.follower, self.following)

    def as_dict(self):
        return {
            # I don't know if this is correct -- this relationship not in example-article.json
            "query": "following",
            "author": self.follower.as_dict(),
            "friend": self.following.as_dict(),
            "date": self.date
        }


class Friend(models.Model):
    # when request was accepted
    date = models.DateTimeField(auto_now_add=True)
    # who followed back
    accepter = models.ForeignKey(Profile, related_name="accepter",primary_key=True)
    # who started following
    requester = models.ForeignKey(Profile, related_name="requester")
    #did accepter accept the request
    accepted = models.BooleanField(default=False)

    def __unicode__(self):
        return u"{} -> {}".format(self.requester, self.accepter)

    def as_dict(self):
        return {
            "query": "friends",
            "author": self.requester.as_dict(),
            "friend": self.accepter.as_dict(),
            "date": self.date
        }
