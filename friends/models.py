from django.db import models
from django.contrib.auth.models import User
from user_profile.models import Profile
# Create your models here.


class Follow(models.Model):
    # when started following
    date = models.DateTimeField(auto_now_add=True)
    # who started following
    follower = models.ForeignKey(Profile, related_name="follower")
    # who was followed
    following = models.ForeignKey(Profile, related_name="following")

    class Meta:
        unique_together = ('follower', 'following')

    def __unicode__(self):
        return u"{} -> {}".format(self.follower.display_name, self.following.display_name)

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
    accepter = models.ForeignKey(Profile, related_name="accepter")
    # who started following
    requester = models.ForeignKey(Profile, related_name="requester")

    def __unicode__(self):
        return u"{} -> {}".format(self.requester, self.accepter)

    def as_dict(self):
        return {
            "query": "friends",
            "author": self.requester.as_dict(),
            "friend": self.accepter.as_dict(),
            "date": self.date
        }

    class Meta:
        unique_together = (('requester', 'accepter'),)

class FriendRequest(models.Model):
    # when request was accepted
    date = models.DateTimeField(auto_now_add=True)
    requester = models.ForeignKey(Profile, related_name="frrequester")
    accepter = models.ForeignKey(Profile, related_name="fraccepter")

    def __unicode__(self):
        return u"{} -> {}".format(self.requester, self.accepter)

    class Meta:
        unique_together = (('requester', 'accepter'),)

