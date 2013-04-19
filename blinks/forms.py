from blinks.models import Link
from django import forms

class LinkForm(forms.ModelForm):
  """Simple form for editing a Link object
  """
  delete = forms.BooleanField(required=False)
  
  class Meta:
    model = Link
    exclude = ('url', 'user',)
    widgets = {
      'order': forms.widgets.HiddenInput()
    }