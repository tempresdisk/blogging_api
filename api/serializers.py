from rest_framework import serializers, validators

from . import models


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = models.Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = models.Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=models.User.objects.all()
    )

    class Meta:
        fields = ('user', 'following')
        model = models.Follow
        validators = [
            validators.UniqueTogetherValidator(
                queryset=models.Follow.objects.all(),
                fields=['user', 'following']
            )
        ]

    def validate_following(self, value):
        user = self.context['request'].user
        if value == user:
            raise serializers.ValidationError("You cannot follow yourself")
        return value


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('title', )
        model = models.Group
