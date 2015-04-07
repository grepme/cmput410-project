# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('host', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('user_header', models.CharField(max_length=40)),
                ('auth_type', models.CharField(max_length=6)),
                ('auth_user', models.CharField(max_length=50)),
                ('auth_password', models.CharField(max_length=50)),
                ('realm', models.CharField(max_length=50)),
                ('author_posts', models.CharField(default=b'/author/posts', max_length=60)),
                ('author_id_posts', models.CharField(default=b'/author/{author_guid}/posts', max_length=60)),
                ('posts', models.CharField(default=b'/posts', max_length=60)),
                ('posts_id', models.CharField(default=b'/posts/{post_guid}', max_length=60)),
                ('posts_id_post', models.CharField(default=b'/posts/{post_guid}', max_length=60)),
                ('friends_id_id', models.CharField(default=b'/friends/{friend_guid}/{friend_2_guid}', max_length=60)),
                ('friends_list', models.CharField(default=b'/friends/{friend_guid}', max_length=60)),
                ('friend_request', models.CharField(default=b'/friendrequest', max_length=60)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
