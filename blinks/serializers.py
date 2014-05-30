from blinks.models import Link
from rest_framework import serializers

class LinkSerializer(serializers.ModelSerializer):
  class Meta:
    model = Link
    fields = ('id', 'title', 'url', 'order')
