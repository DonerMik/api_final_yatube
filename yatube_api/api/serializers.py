from rest_framework import serializers
from rest_framework.relations import SlugRelatedField, PrimaryKeyRelatedField
from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_object_or_404

from posts.models import Comment, Group, Post, Follow, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')
        model = Post


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'descriptions',)


class CommentSerializer(serializers.ModelSerializer):
    post = PrimaryKeyRelatedField(required=False, read_only=True, many=False)
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(slug_field='username', read_only=True)
    following = SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate(self, attrs):
        user = self.context['request'].user
        following = attrs['following']
        if user == following:
            raise serializers.ValidationError(
                'Ошибка подписки!')
        if Follow.objects.filter(user=user,
                                 following=following).exists():
            raise serializers.ValidationError(
                'Данная подписка существует'
            )
        return attrs
