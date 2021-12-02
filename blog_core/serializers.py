from rest_framework import serializers

from blog_core.models import Post, Comment
from blog_core.utils import APIPostMixin


class CommentCreateSerializer(APIPostMixin, serializers.ModelSerializer):
    post = serializers.SlugRelatedField(slug_field='title', write_only=True, queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ('id', 'content', 'author', 'post')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'content')


class PostListSerializer(APIPostMixin, serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author')


class PostDetailSerializer(APIPostMixin, serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        exclude = ('slug',)
