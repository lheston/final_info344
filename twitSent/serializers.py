from django.forms import widgets
from rest_framework import serializers
from .models import Post

class UrlsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ('tweetContent', 'name', 'sent', 'bad')


def create(self, validated_data):
	"""
	Create and return a new 'web' instance, given the validated validated_data
	"""
	return retUrl.objects.create(**validated_data)

def update(self, instance, validated_data):
	"""
	Update and return an existing url instance, given the validated validated_data
	"""
	instance.pk = validated_data.get('pk', instance.created)
	instance.tweetContent = validated_data.get('tweetContent', instance.created)
	instance.name = validated_data.get('name', instance.created)
	instance.sent = validated_data.get('sent', instance.created)
	instance.bad = validated_data.get('bad', instance.created)
	return instance

