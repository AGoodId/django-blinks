from blinks.forms import LinkForm
from blinks.models import Link

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
  
