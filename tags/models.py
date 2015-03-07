from django.db import models

# Create your models here.


class Tag(models.Model):

    name = models.CharField(max_length=55)

    def __unicode__(self):
        return self.name