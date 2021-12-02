from rest_framework import serializers

from blog_core.models import Post, Comment
from blog_core.utils import APIAuthorMixin


class PostListSerializer(APIAuthorMixin, serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author')


class CommentCreateSerializer(APIAuthorMixin, serializers.ModelSerializer):
    post = serializers.SlugRelatedField(slug_field='title', write_only=True, queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ('id', 'content', 'author', 'post')


class CommentSerializer(APIAuthorMixin, serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'author', 'content')


class PostDetailSerializer(APIAuthorMixin, serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        exclude = ('slug',)
