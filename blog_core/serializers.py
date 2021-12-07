from django.shortcuts import get_object_or_404
from rest_framework import serializers

from blog_core.models import Comment, Post
from users.models import CustomUser


class PostListSerializer(serializers.ModelSerializer):
    """Serializer to show list of posts."""

    author_name = serializers.CharField(source='author.username')

    class Meta:
        """Provide PostListSerializer settings."""

        model = Post
        fields = ('id', 'title', 'content', 'author_name')

    def create(self, validated_data: dict) -> Post:
        """Update author field in the validated_data and create new post.

        Args:
            validated_data: POST validated data

        Returns:
            Create new post
        """
        validated_data['author'] = get_object_or_404(CustomUser, username=validated_data['author']['username'])
        return Post.objects.create(**validated_data)


class CommentCreateSerializer(serializers.ModelSerializer):
    """Serializer to create comments."""

    post = serializers.SlugRelatedField(
        slug_field='title',
        queryset=Post.objects.prefetch_related('author', 'comments__author'),
    )
    author_name = serializers.CharField(source='author.username')

    class Meta:
        """Provide CommentCreateSerializer settings."""

        model = Comment
        fields = ('id', 'content', 'author_name', 'post')

    def create(self, validated_data: dict) -> Comment:
        """Update author field in the validated_data and create new comment.

        Args:
            validated_data: POST validated data

        Returns:
            Create new comment
        """
        validated_data['author'] = get_object_or_404(CustomUser, username=validated_data['author']['username'])
        return Comment.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    """Serializer to add comments section."""

    author_name = serializers.CharField(source='author.username')

    class Meta:
        """Provide CommentSerializer settings."""

        model = Comment
        fields = ('id', 'author_name', 'content')


class PostDetailSerializer(serializers.ModelSerializer):
    """Serializer to show detailed post."""

    author_name = serializers.CharField(source='author.username')
    comments = CommentSerializer(many=True)

    class Meta:
        """Provide PostDetailSerializer settings."""

        model = Post
        exclude = ('slug', 'author')
