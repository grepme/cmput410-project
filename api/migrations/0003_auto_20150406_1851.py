# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_server_api_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='author',
            field=models.CharField(default=b'/author', max_length=60),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='server',
            name='author_id',
            field=models.CharField(default=b'/author/{author_id}', max_length=60),
            preserve_default=True,
        ),
    ]
