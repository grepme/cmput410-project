# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='posts_id_post',
            field=models.CharField(default=b'/posts/{post_guid}', max_length=60),
            preserve_default=True,
        ),
    ]
