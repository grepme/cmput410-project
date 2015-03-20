from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

# Create your models here.


class Comment(models.Model):
    date = models.DateTimeField()
    # Not sure how to make a "content" field either text or image
    text = models.CharField(max_length=63206, blank=True)
    image = models.ImageField(blank=True)
    post = models.ForeignKey(Post)
    author = models.ForeignKey(User)

    # guid
    guid = models.CharField(max_length=55, default=None)

    def __unicode__(self):
        return self.text[:10]

    def as_dict(self):
        return {
        	"author": Profile.objects.get(author=self.author).as_dict(),
        	"comment": self.text,
        	"pubDate": self.date,
        	"guid": self.guid,
            # not in example-article.json... Do we need these?
            "post": Post.objects.get(post=self.post).as_dict(),
            "image": self.image
            }
