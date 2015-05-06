from django.conf.urls import patterns, include, url
#from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'do_classroom.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

#    url(r'^admin/', include(admin.site.urls)),
#    url('^', include('django.contrib.auth.urls')),
    url(r'^logout/', 'do_classroom.classes.views.logout_view', name='logout'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^complete/digitalocean/', 'do_classroom.classes.views.login_complete', name='login_complete'),
    url(r'^$', 'do_classroom.classes.views.home', name='home'),
    url(r'^class/new', 'do_classroom.classes.views.new_class', name='new_class'),
    url(r'^class/(?P<class_prefix>\w+)/$', 'do_classroom.classes.views.class_view', name='class'),
)
