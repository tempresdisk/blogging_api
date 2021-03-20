from rest_framework import viewsets, mixins
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from . import models
from .permissions import IsAuthorOrReadOnly
from . import serializers


class PostViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]
    filterset_fields = ('group', )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return models.Comment.objects.filter(post_id=post_id)


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = serializers.FollowSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ('user__username', 'following__username')
    search_fields = ('user__username', 'following__username')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return models.Follow.objects.all()
        return user.following.all()


class GroupViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = models.Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
