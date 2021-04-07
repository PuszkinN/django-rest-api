from rest_framework import serializers
from content.models import *


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class MovieCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'video', 'description', 'is_premium']
    
    def create(self, validated_data):
        movie = Post.objects.create(
            title = validated_data['title'],
            video = self.context.get('request').FILES,
            author = self.context.get('request').user,
            description = validated_data['description'],
            is_premium = validated_data['is_premium']
        )
        movie.save()
        return movie
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class CommentSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    class Meta:
        model = Comment
        fields = '__all__'

class CreateCommentSerializer(serializers.ModelSerializer):
    # timestamp = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    class Meta:
        model = Comment
        fields = ['body']
    
    def create(self, validated_data):
        comment = Comment.objects.create(
            body=validated_data.get('body'),
            movie=self.context.get('movie'),
            author=self.context.get('request').user
        )
        comment.save()

        return comment

    def update(self, instance, validated_data):
        instance.body = validated_data['body']
        instance.edited = True
        instance.save()
        return instance


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'

class ImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['image']
    
    def create(self):
        photo, created = Photo.objects.get_or_create(
            author=self.context.get('request.user', None),
            image=self.context.get('request.FILES', None)
        )

        photo.save()
        return photo