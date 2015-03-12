from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    author = models.ForeignKey(User)
    display_name = models.CharField(max_length=55)

    # guid
    guid = models.CharField(max_length=55, default=None)

    def as_dict(self):
        return { 
        	"id": self.guid,
        	# TODO implement host
            "host": ""
            "displayname" : self.display_name,
            "url": self.host + "/author/" + self.guid
        }
