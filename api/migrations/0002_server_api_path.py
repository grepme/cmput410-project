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
            name='api_path',
            field=models.CharField(default=b'', max_length=50),
            preserve_default=True,
        ),
    ]
