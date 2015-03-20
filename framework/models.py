from django.db import models
import uuid

# Create your models here.

# Guid model use this instead of defining the guid in each model...

class GUIDModel(models.Model):
    guid = models.CharField(primary_key=True, max_length=55)
    def save(self, *args, **kwargs):
      if not self.guid:
        self.guid = uuid.uuid1().__str__()
      super(GUIDModel, self).save(*args, **kwargs)
