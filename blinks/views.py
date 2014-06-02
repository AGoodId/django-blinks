from blinks.forms import LinkForm
from blinks.models import Link
from blinks.serializers import LinkSerializer
import django_filters
from rest_framework import generics, permissions, filters


from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import loader, RequestContext
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST


@require_POST
@login_required
def add(request):
  """Extracts parameters from a GET request and creates a new Link object for
  the currently logged in user.
  """
  user = request.user
  path = request.POST.get('path', None)
  title = request.POST.get('title', None)
  if not path or not title:
    t = loader.get_template("403.html")
    return HttpResponseForbidden(t.render(RequestContext(request, {})))

  links = Link.objects.filter(user=user).order_by('-order')
  try:
    order = links[0].order+1
  except IndexError:
    order = 0
  link_attrs = {'title': title,
                'url': path,
                'user': user,
                'order': order}
  new_link = Link(**link_attrs)
  new_link.save()
  new_link.sites.add(settings.SITE_ID)
  messages.add_message(request, messages.SUCCESS, _('Your bookmark was added'))
  return HttpResponseRedirect(path)


@login_required
def change(request):
  """Bulk change view for all links for a user.
  """
  user = request.user
  links = Link.objects.filter(user=user)
  if request.method == 'POST':
    # Save forms
    forms = [LinkForm(request.POST, instance=l, prefix=str(l.pk)) for l in links]
    if all(f.is_valid() for f in forms):
      for f in forms:
        if f.cleaned_data['delete'] == True:
          messages.add_message(request, messages.SUCCESS, _('Your bookmark was deleted'))
          f.instance.delete()
        else:
          f.save()
      # Fetch reordered list of forms and message user
      links = Link.objects.filter(user=user)
      forms = [LinkForm(request.POST, instance=l, prefix=str(l.pk)) for l in links]
      messages.add_message(request, messages.SUCCESS, _('Your bookmarks were updated'))
    else:
      # Inform user of error
      messages.add_message(request, messages.ERROR, _('Something went wrong. Check below for details and try again.'))
  else:
    forms = [LinkForm(instance=l, prefix=str(l.pk)) for l in links]
  return render_to_response('blinks/change.html',
                            locals(),
                            context_instance=RequestContext(request))


class IsOwner(permissions.BasePermission):
  """Object-level permission to only allow the owner of an object to view and edit it.
  """
  def has_object_permission(self, request, view, obj):
    return obj.user == request.user


class IsOwnerFilterBackend(filters.BaseFilterBackend):
  """Filter that only allows users to see their own objects.
  """
  def filter_queryset(self, request, queryset, view):
    return queryset.filter(user=request.user)


class LinkListAPIView(generics.ListCreateAPIView):
  """List API for links that allows listing and creating.
  """
  queryset = Link.objects.all()
  serializer_class = LinkSerializer
  paginate_by = 10
  max_paginate_by = 100
  paginate_by_param = 'limit'
  permission_classes = (permissions.IsAuthenticated,)
  filter_backends = (IsOwnerFilterBackend,)

  def pre_save(self, obj):
    # Set the current user as author
    obj.user = self.request.user

  def post_save(self, obj, created=False):
    # Add to the current site
    obj.sites.add(settings.SITE_ID)


class LinkDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
  """Detail API for links that allows viewing and editing.
  """
  model = Link
  serializer_class = LinkSerializer
  permission_classes = (permissions.IsAuthenticated, IsOwner,)
  
  def pre_save(self, obj):
    # Set the current user as owner
    obj.user = self.request.user
  
  def post_save(self, obj, created=False):
    # Add to the current site
    obj.sites.add(settings.SITE_ID)
