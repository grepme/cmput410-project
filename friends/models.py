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

    def as_dict(self):
        return {
            # I don't know if this is correct -- this relationship not in example-article.json
            "query": "following",
            "author": Profile.objects.get(author=self.follower).as_dict(),
            "friend": Profile.objects.get(author=self.following).as_dict(),
            "date": self.date
        }


class Friend(models.Model):
    # when request was accepted
    date = models.DateTimeField(auto_now_add=True)
    # who followed back
    accepter = models.ForeignKey(User, related_name="accepter")
    # who started following
    requester = models.ForeignKey(User, related_name="requester")
    #did accepter accept the request
    accepted = models.BooleanField(default=False)

    def __unicode__(self):
        return u"{} -> {}".format(self.requester, self.accepter)

    def as_dict(self):
        return {
            "query": "friends",
            "author": Profile.objects.get(author=self.requester).as_dict(),
            "friend": Profile.objects.get(author=self.accepter).as_dict(),
            "date": self.date
        }
