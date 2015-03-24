from django.db import models
from django.contrib.auth.models import User
import uuid
import time


# Create your models here.

# using the guid model
from framework.models import GUIDModel

class Profile(GUIDModel):
    author = models.ForeignKey(User)
    display_name = models.CharField(max_length=55)

    # Set to yes is profile is hosted else where
    is_external = models.BooleanField(default=False)

    # TODO don't use hardcoded host, should be of running instance
    host = models.CharField(max_length=55)

    def as_dict(self):
        return {
            "id": self.guid,
        	# TODO implement host
            "host": "",
            "displayname" : self.display_name,
            "url": self.host + "/author/" + self.guid
        }
