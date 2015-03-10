from django.db import models
from django.contrib.auth.models import User
from tags.models import Tag
from user_profile.models import Profile
import uuid
from json import JSONEncoder, dumps

# Create your models here.
class PostEncoder(JSONEncoder):
        def default(self, o):
            return o.as_dict() 

class Post(models.Model):
    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        if not self.guid:
            self.guid = uuid.uuid1().__str__()
        #self.guid = self.guid.replace("-", "_")

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
    image  = models.ImageField(blank=True, upload_to='images/%Y/%m/%d')
    origin = models.GenericIPAddressField()
    source = models.GenericIPAddressField()
    author = models.ForeignKey(User)
    # whether or not they used commonmark
    commonmark = models.BooleanField(default=False)

    # Tags that can be used to filter posts
    tags = models.ManyToManyField(Tag, blank=True)
    visibility = models.IntegerField(choices=visibilityChoices)

    # guid
    guid = models.CharField(max_length=55, default=None)

    def visibility_string(self):
        return Post.visibilityChoices[self.visibility][1]

    def as_dict(self): 
        return {
            "title": self.title,
            "source": self.source,
            "origin": self.origin,
            # TODO: implement description
            "description": "",
            "content-type": self.get_content_type(),
            "content": self.text,
            "author": Profile.objects.get(author=self.author).as_dict(),
            "categories": list(self.tags.all()),
            "comments": list(), 
            "pubDate": self.date,
            "guid": self.guid, 
            "visibility": self.visibility_string()
            }   

    def to_json(self):
        return json.dumps(self,cls=PostEncoder)

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
