from rest_framework import serializers

from blog_core.models import Comment, Post
from users.models import CustomUser


class PostListSerializer(serializers.ModelSerializer):
    """Serializer to show list of posts."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=CustomUser.objects.all(),
    )

    class Meta:
        """Provide PostListSerializer settings."""

        model = Post
        fields = ('id', 'title', 'content', 'author')


class CommentCreateSerializer(serializers.ModelSerializer):
    """Serializer to create comments."""

    post = serializers.SlugRelatedField(slug_field='title', write_only=True, queryset=Post.objects.all())
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=CustomUser.objects.all(),
    )

    class Meta:
        """Provide CommentCreateSerializer settings."""

        model = Comment
        fields = ('id', 'content', 'author', 'post')


class CommentSerializer(serializers.ModelSerializer):
    """Serializer to add comments section."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        """Provide CommentSerializer settings."""

        model = Comment
        fields = ('id', 'author', 'content')


class PostDetailSerializer(serializers.ModelSerializer):
    """Serializer to show detailed post."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    comments = CommentSerializer(many=True)

    class Meta:
        """Provide PostDetailSerializer settings."""

        model = Post
        exclude = ('slug',)
