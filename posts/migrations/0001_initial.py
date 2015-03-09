# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=55)),
                ('date', models.DateTimeField()),
                ('text', models.CharField(max_length=63206, blank=True)),
                ('image', models.ImageField(upload_to=b'/images/', blank=True)),
                ('origin', models.GenericIPAddressField()),
                ('source', models.GenericIPAddressField()),
                ('visibility', models.IntegerField(choices=[(1, b'Private'), (2, b'Friend'), (3, b'Friend of A Friend'), (4, b'Server'), (5, b'Public')])),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(to='tags.Tag', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
