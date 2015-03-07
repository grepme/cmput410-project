from django.db import models

# import all of the models from each app
from comments.models import Comment
from friends.models import Friend, Follow
from posts.models import Post
from tags.models import Tag
from django.contrib.auth.models import User
