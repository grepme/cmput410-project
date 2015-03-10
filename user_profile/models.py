from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    author = models.ForeignKey(User)
    display_name = models.CharField(max_length=55)

    def as_dict(self):
        return { "id": self.author.id,
                # Needs to be added "host": 
                "displayname" : self.display_name,
                # "url" : TODO: implement url and host 
                }
