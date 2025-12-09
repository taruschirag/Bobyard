from django.utils import timezone
from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'date', 'likes', 'image']
        read_only_fields = ['id', 'author', 'date', 'likes']

    def create(self, validated_data):
        return Comment.objects.create(
            author='Admin',
            date=timezone.now(),
            likes=0,
            **validated_data,
        )

    def update(self, instance, validated_data):
        update_fields = []
        if 'text' in validated_data:
            instance.text = validated_data['text']
            update_fields.append('text')
        if 'image' in validated_data:
            instance.image = validated_data['image']
            update_fields.append('image')

        if update_fields:
            instance.save(update_fields=update_fields)
        else:
            instance.save()
        return instance
