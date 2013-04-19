from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _


class Link(models.Model):
  """
  A link with a title, sort order and a connection to the user who created it.
  """
  title = models.CharField(_('title'), max_length=255)
  url = models.CharField(_('URL'), max_length=255)
  user = models.ForeignKey(User, verbose_name=_('author'))
  order = models.PositiveIntegerField(_('order'))

  objects = models.Manager()

  class Meta:
    verbose_name = _('link')
    verbose_name_plural = _('links')
    ordering = ['user', 'order']

  def __unicode__(self):
    return self.title
