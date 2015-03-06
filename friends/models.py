from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Follow(models.Model):
    # when started following
    date = models.DateTimeField()
    # who started following
    follower = models.ForeignKey(User, related_name="follower")
    # who was followed
    following = models.ForeignKey(User, related_name="following")

    def __unicode__(self):
        return u"{} -> {}".format(self.follower, self.following)


class Friend(models.Model):
    # when request was accepted
    date = models.DateTimeField()
    # who followed back
    accepter = models.ForeignKey(User, related_name="accepter")
    # who started following
    requester = models.ForeignKey(User, related_name="requester")

    def __unicode__(self):
        return u"{} -> {}".format(self.requester, self.accepter)