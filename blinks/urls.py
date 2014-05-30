from django.conf.urls.defaults import *

from blinks.views import LinkListAPIView, LinkDetailAPIView

urlpatterns = patterns('blinks.views',
  url(r'^add/$', 'add', name='add'),
  url(r'^edit/$', 'change', name='change'),
  url(r'^api/?$', LinkListAPIView.as_view()),
  url(r'^api/(?P<pk>[0-9]+)/?$', LinkDetailAPIView.as_view()),
)
