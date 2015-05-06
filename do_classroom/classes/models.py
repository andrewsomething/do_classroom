from django.db import models
from django.contrib.auth.models import User

import string, random

def prefix_generator(size=8):
    return ''.join(random.choice(string.ascii_lowercase +
        string.digits) for _ in range(size))


class Teacher(models.Model):
    user = models.OneToOneField(User)
    email = models.CharField(max_length=200)
    uuid = models.CharField(max_length=200)
    droplet_limit = models.IntegerField()

    def _token(self):
        douser = self.user.social_auth.get(provider='digitalocean')
        return douser.access_token
    token = property(_token)

class Class(models.Model):
    teacher = models.ForeignKey(Teacher)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    destroyed_at = models.DateTimeField(null=True)
    name = models.CharField(max_length=200)
    class_size = models.IntegerField(default=1)
    prefix = models.CharField(max_length=15, default=prefix_generator)

    packages = models.TextField(default=" ")
    droplet_image = models.CharField(max_length=50)
    droplet_size = models.CharField(max_length=25)
    droplet_region = models.CharField(max_length=50)
    droplet_priv_net = models.BooleanField(default=False)
    droplet_ipv6 = models.BooleanField(default=False)

    def _is_active(self):
        if not self.destroyed_at:
            return True
    is_active = property(_is_active)

class Droplet(models.Model):
    group = models.ForeignKey(Class)
    droplet_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    destroyed_at = models.DateTimeField(null=True)
    initial_pwd = models.CharField(max_length=50)

    def _image(self):
        return self.group.droplet_image
    image = property(_image)

    def _size(self):
        return self.group.droplet_size
    size = property(_size)

    def _region(self):
        return self.group.droplet_region
    region = property(_region)
