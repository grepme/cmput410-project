from django.db import models
from django.contrib.auth.models import User
from tags.models import Tag
from user_profile.models import Profile
import uuid
import json

# using the guid model
from framework.models import GUIDModel

# Create your models here.
class PostEncoder(json.JSONEncoder):
    def default(self, o):
        return o.as_dict()


class Post(GUIDModel):
    private = 1
    friend = 2
    FOAF = 3
    server = 4
    public = 5
    visibilityChoices = (
        (private, 'PRIVATE'),
        (friend, 'FRIEND'),
        (FOAF, 'FOAF'),
        (server, 'SERVER'),
        (public, 'PUBLIC'),
    )

    # 55 characters is (usually) enough to show up in a Google search
    title = models.CharField(max_length=55)
    date = models.DateTimeField()
    # Not sure how to make a "content" field either text or image
    text = models.CharField(max_length=63206, blank=True)
    image = models.ImageField(blank=True, upload_to='images/%Y/%m/%d')
    origin = models.GenericIPAddressField()
    source = models.GenericIPAddressField()
    author = models.ForeignKey(Profile)
    # whether or not they used commonmark
    commonmark = models.BooleanField(default=False)

    # Tags that can be used to filter posts
    tags = models.ManyToManyField(Tag, blank=True)
    visibility = models.IntegerField(choices=visibilityChoices)

    def visibility_string(self):
        return Post.visibilityChoices[self.visibility - 1][1]

    def comments_to_list(self):
        from comments.models import Comment

        comments = Comment.objects.filter(post=self)
        comment_list = []
        for comment in comments:
            comment_list.append(comment.as_dict())

        return comment_list

    def as_dict(self):

        comments = self.comments_to_list()
        return {
            "title": self.title,
            "source": self.source,
            "origin": self.origin,
            # TODO: implement description
            "description": self.text[:10],
            "content-type": self.get_content_type(),
            "content": self.text,
            "author": self.author.as_dict(),
            "categories": list(self.tags.all()),
            "comments": comments,
            "pubDate": self.date,
            "guid": self.guid,
            "visibility": self.visibility_string()
        }

    def to_json(self):
        return json.dumps(self, cls=PostEncoder)

    def get_content_type(self):
        if self.commonmark:
            return "text/x-markdown"
        else:
            return "text/plain"


    @staticmethod
    def get_visibility(visibility):
        for visible_choice in Post.visibilityChoices:
            if visible_choice[1] == visibility:
                return visible_choice[0]

    def __unicode__(self):
        return self.title
