# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import do_classroom.classes.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('destroyed_at', models.DateTimeField(null=True)),
                ('name', models.CharField(max_length=200)),
                ('class_size', models.IntegerField(default=1)),
                ('prefix', models.CharField(default=do_classroom.classes.models.prefix_generator, max_length=15)),
                ('packages', models.TextField(default=b' ')),
                ('droplet_image', models.CharField(max_length=50)),
                ('droplet_size', models.CharField(max_length=25)),
                ('droplet_region', models.CharField(max_length=50)),
                ('droplet_priv_net', models.BooleanField(default=False)),
                ('droplet_ipv6', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Droplet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('droplet_id', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('destroyed_at', models.DateTimeField(null=True)),
                ('initial_pwd', models.CharField(max_length=50)),
                ('group', models.ForeignKey(to='classes.Class')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(max_length=200)),
                ('uuid', models.CharField(max_length=200)),
                ('droplet_limit', models.IntegerField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='class',
            name='teacher',
            field=models.ForeignKey(to='classes.Teacher'),
            preserve_default=True,
        ),
    ]
