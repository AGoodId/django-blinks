from django.conf.urls.defaults import *

urlpatterns = patterns('blinks.views',
  url(ur'^add/$', 'add', name='add'),
  url(ur'^edit/$', 'change', name='change'),
)
