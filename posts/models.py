from django.db import models
from django.contrib.auth.models import User

# Create your models here.

@login_required
class Post(models.Model):
    private = 1
    friend = 2
    FOAF = 3
    server = 4
    public = 5
    visibilityChoices = (
        (private, 'Private'),
        (friend, 'Friend'),
        (FOAF, 'Friend of A Friend'),
        (server, 'Server'),
        (public, 'Public'),
    )

    # 55 characters is (usually) enough to show up in a Google search
    title = models.CharField(max_length=55)
    date = models.DateTimeField()
    # Not sure how to make a "content" field either text or image
    text = models.CharField(max_length=63206, blank=True)
    image = models.ImageField(blank=True, upload_to='/images/')
    origin = models.GenericIPAddressField()
    source = models.GenericIPAddressField()
    author = models.ForeignKey(User)
    # Can't store arrays of strings, so have to do this a custom way
    # http://cramer.io/2008/08/08/custom-fields-in-django/
    # categories = SeperatedValuesField(blank=True)
    visibility = models.IntegerField(choices=visibilityChoices)

    def __unicode__(self):
        return self.title