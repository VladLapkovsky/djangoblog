from rest_framework import serializers

from blog_core.models import Post, Comment
from users.models import CustomUser


class PostListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=CustomUser.objects.all(),
    )

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author')


class CommentCreateSerializer(serializers.ModelSerializer):
    post = serializers.SlugRelatedField(slug_field='title', write_only=True, queryset=Post.objects.all())
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=CustomUser.objects.all(),
    )

    class Meta:
        model = Comment
        fields = ('id', 'content', 'author', 'post')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'content')


class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        exclude = ('slug',)
