from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

# using the guid model
from framework.models import GUIDModel

class Profile(GUIDModel):
    author = models.ForeignKey(User)
    display_name = models.CharField(max_length=55)

    # TODO don't use hardcoded host, should be of running instance
    host = models.CharField(max_length=55,default="http://localhost:8000")

    def as_dict(self):
        return {
            "id": self.guid,
        	# TODO implement host
            "host": "",
            "displayname" : self.display_name,
            "url": self.host + "/author/" + self.guid
        }
