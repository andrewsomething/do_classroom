from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django import forms

from forms import NewClassForm
from models import Teacher, Class, Droplet
from utils.do_tools import launch_droplets, add_droplet, power_off, power_on, list_droplets, destroy, end_class

import digitalocean
import re

def login_complete(request):
    return redirect('/')

def logout_view(request):
    logout(request)
    return redirect('/')

def home(request):
    if request.user.is_authenticated():
        teacher = Teacher.objects.get(user=request.user)
        classes = []
        for c in Class.objects.filter(teacher=teacher):
            if c.is_active:
                classes.append(c)
        return render(request, 'index.html', {'classes': classes,
                                              'acct': teacher})
    else:
        return render(request, 'index.html', {})

@login_required()
def new_class(request):
    if request.method == 'POST':
        form = NewClassForm(request.POST)
        if form.is_valid():
            pkgs = re.findall(r'[^,;\s]+', form.cleaned_data['packages'])
            new_class = Class(teacher = Teacher.objects.get(user=request.user),
                              name = form.cleaned_data['name'],
                              class_size = form.cleaned_data['class_size'],
                              droplet_image = form.cleaned_data['droplet_image'],
                              droplet_size = form.cleaned_data['droplet_size'],
                              droplet_region = form.cleaned_data['droplet_region'],
                              packages=' '.join(pkgs))
                              # droplet_priv_net = form.cleaned_data['droplet_priv_net'],
                              # droplet_ipv6 = form.cleaned_data['droplet_ipv6'])
            new_class.save()
            launch_droplets(request, new_class)
            return redirect('/class/' + new_class.prefix)
        else:
            return HttpResponse(form.errors)
    else:
        form = NewClassForm()
        teacher = Teacher.objects.get(user=request.user)
        return render(request, 'new_class.html',
                     {'form': form, 'acct': teacher})

@login_required()
def class_view(request, class_prefix):
    teacher =Teacher.objects.get(user=request.user)
    token = teacher.token

    if request.method == "POST" and request.is_ajax():
        print request.POST
        if 'droplet' in request.POST:
            droplet_id = request.POST['droplet']
        if request.POST['action'] == 'off':
            power_off(token, droplet_id)
        elif request.POST['action'] == 'on':
            power_on(token, droplet_id)
        elif request.POST['action'] == 'destroy':
            destroy(token, droplet_id)
        elif request.POST['action'] == 'add-droplet':
            class_obj = Class.objects.get(prefix=class_prefix)
            add_droplet(token, class_obj)
        elif request.POST['action'] == 'end-class':
            class_obj = Class.objects.get(prefix=class_prefix)
            end_class(token, class_obj)
        else:
            print "Something went wrong here...."

    droplets = list_droplets(token, class_prefix)
    class_obj = Class.objects.get(prefix=class_prefix)
    return render(request,
                  'class.html',
                  {'class': class_obj,
                  'droplets': droplets,
                  'acct': teacher})