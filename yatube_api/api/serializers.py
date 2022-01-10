from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField, SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post, User


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
    user = SlugRelatedField(slug_field='username', read_only=True, default=serializers.CurrentUserDefault())
    following = SlugRelatedField(slug_field='username',
                                 queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ('user', 'following')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            ),
        ]

    def validate_following(self, value):
        user = self.context['request'].user
        if value == user:
            raise serializers.ValidationError(
                'Ошибка подписки!')
        return value
