from django.db import models
from django.contrib.auth.models import User
from tags.models import Tag
import uuid

# Create your models here.


class Post(models.Model):
    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        if not self.guid:
            self.guid = uuid.uuid1().__str__()


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
    image = models.ImageField(blank=True, upload_to='images/%Y/%m/%d')
    origin = models.GenericIPAddressField()
    source = models.GenericIPAddressField()
    author = models.ForeignKey(User)
    # whether or not they used commonmark
    commonmark = models.BooleanField(default=False)

    # Tags that can be used to filter posts
    tags = models.ManyToManyField(Tag, blank=True)
    visibility = models.IntegerField(choices=visibilityChoices)

    # guid
    guid = models.CharField(max_length=55)

    @staticmethod
    def get_visibility(visibility):
        for visible_choice in Post.visibilityChoices:
            if visible_choice[1] == visibility:
                return visible_choice[0]

    def __unicode__(self):
        return self.title