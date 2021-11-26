"""blog_core models configuration."""

from django.db import models
from django.urls import reverse

from users.models import CustomUser


class Post(models.Model):
    """Blog Post model."""

    title = models.CharField(max_length=255, verbose_name='post title')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(verbose_name='post content')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='published')
    rating = models.IntegerField(default=0, verbose_name='post rating')
    author = models.ForeignKey(
        CustomUser,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='author',
    )

    def __str__(self) -> str:
        """Return post title.

        Returns:
            post title
        """
        return self.title

    def get_absolute_url(self) -> str:
        """Return absolute slug URL.

        Returns:
            absolute url
        """
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        """Add additional parameters to the Post model."""

        verbose_name_plural = 'posts'
        verbose_name = 'post'
        ordering = ['-published']


class Comment(models.Model):
    """Blog Comment model."""

    content = models.TextField(verbose_name='comment content')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='published')
    rating = models.IntegerField(default=0, verbose_name='comment rating')
    author = models.ForeignKey(
        CustomUser,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='author',
    )
    post = models.ForeignKey(
        Post,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='post',
    )

    def __str__(self) -> str:
        """Return comment author username.

        Returns:
            post title
        """
        return str(self.author)

    class Meta:
        """Add additional parameters to the Comment model."""

        verbose_name_plural = 'comments'
        verbose_name = 'comment'
        ordering = ['-published']
