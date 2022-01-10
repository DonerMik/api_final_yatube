from django.shortcuts import get_object_or_404
from posts.models import Comment, Follow, Group, Post, User
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAuthorOrReadOnlyPermission
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnlyPermission]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnlyPermission]

    def get_queryset(self):
        pk = int(self.kwargs.get('post_id'))
        get_object_or_404(Post, pk=pk)
        queryset = Comment.objects.filter(post__pk=pk)
        return queryset

    def perform_create(self, serializer):
        pk = int(self.kwargs.get('post_id'))
        post = get_object_or_404(Post, pk=pk)
        serializer.save(author=self.request.user,
                        post=post)


class FollowViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        user = self.request.user
        following = Follow.objects.filter(user__username=user)
        # не понимаю как именно тут related_name реализовать еще
        # оригинальная документация DRF работает?
        return following

    def perform_create(self, serializer):
        following = serializer.validated_data.get('following')
        username_following = get_object_or_404(User, username=following)
        serializer.save(user=self.request.user,
                        following=username_following)
