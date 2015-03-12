from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


class Profile(models.Model):
    def __init__(self, *args, **kwargs):
        super(Profile, self).__init__(*args, **kwargs)
        if not self.guid:
            self.guid = uuid.uuid1().__str__()

    author = models.ForeignKey(User)
    display_name = models.CharField(max_length=55)

    # guid
    guid = models.CharField(max_length=55, default=None)

    def as_dict(self):
        return {
        	"id": self.guid,
        	# TODO implement host
            "host": "",
            "displayname" : self.display_name,
            "url": self.host + "/author/" + self.guid
        }
