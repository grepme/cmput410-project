from django.db import models
from django.contrib.auth.models import User
import uuid
import time


# Create your models here.

# using the guid model
from framework.models import GUIDModel
from django.conf import settings

CUSTOM_HOST_DEFAULT = settings.CUSTOM_HOST_DEFAULT


class Profile(GUIDModel):
    author = models.ForeignKey(User, null=True)
    display_name = models.CharField(max_length=55)

    # Set to yes is profile is hosted else where
    is_external = models.BooleanField(default=False)
    # Last time profile was updated with external server
    last_updated = models.DateTimeField(null=True)

    # TODO don't use hardcoded host, should be of running instance
    host = models.CharField(max_length=55, null=True, default=CUSTOM_HOST_DEFAULT)

    # TODO: Figure out if 55 characters is enough for a Github username
    github_name = models.CharField(max_length=55)

    def as_dict(self):
        return {
            "id": self.guid,  # TODO implement host
            "host": self.host,
            "displayname": self.display_name,
            "url": self.host + "/author/" + self.guid,
            "github_name": self.github_name
        }
