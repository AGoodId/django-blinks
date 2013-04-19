from blinks.models import Link
from django import template

register = template.Library()

def blinks_links(user):
  links = Link.objects.filter(user=user)
  return {'links': links}

def add_blinks_link(path):
  return {'path': path}

register.inclusion_tag('blinks/links.html')(blinks_links)
register.inclusion_tag('blinks/add.html')(add_blinks_link)
