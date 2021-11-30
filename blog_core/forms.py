"""This module provides forms for the blog_core app.

AddPostForm - form to add new posts.
RegisterUserForm - form to register new user.
LoginUserForm - form for user log in.
CommentForm - form to add new comments.
"""
import pydantic
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from blog_core.models import Comment, CustomUser, Post
from blog_core.utils import FormStyleClassMixin
from blog_core.views_handlers import NewPostContent

TITLE_WIDGET = forms.TextInput(
    attrs={
        'placeholder': 'Title example',
    },
)
CONTENT_WIDGET = forms.Textarea(
    attrs={
        'placeholder': 'Hello world!',
    },
)


class AddPostForm(FormStyleClassMixin, forms.ModelForm):
    """Form to add new posts."""

    class Meta:
        """Provide AddPostForm settings."""

        model = Post
        fields = ('title', 'content')
        widgets = {
            'title': TITLE_WIDGET,
            'content': CONTENT_WIDGET,
        }

    def clean_title(self) -> str:
        """Validate new post title for correctness.

        Returns:
            Validated title

        Raises:
            ValidationError: if title is not correct
        """
        try:
            new_post = NewPostContent(title=self.cleaned_data['title'])
        except pydantic.ValidationError as error:
            raise ValidationError(error.raw_errors[0].exc)
        return new_post.title


class RegisterUserForm(FormStyleClassMixin, UserCreationForm):
    """Form to register new users.

    Uses CustomUser model and captcha field.
    """

    captcha = CaptchaField()

    class Meta:
        """Provide RegisterUserForm settings."""

        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self) -> str:
        """Check if a new user's username exists.

        Returns:
            Checked username

        Raises:
            ValidationError: if user with this username already exists
        """
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('The user with this name is already exists. Try another one.')
        return username

    def clean_email(self) -> str:
        """Check if a new user's email exists.

        Returns:
            Checked username

        Raises:
            ValidationError: if user with this email already exists
        """
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('The user with this email is already exists. Try another one.')
        return email


class LoginUserForm(FormStyleClassMixin, AuthenticationForm):
    """Form for user log in."""


COMMENT_WIDGET = forms.Textarea(
    attrs={
        'placeholder': 'Leave your comment',
        'rows': 3,
    },
)


class CommentForm(FormStyleClassMixin, forms.ModelForm):
    """Form to add new comments."""

    class Meta:
        """Provide CommentForm settings."""

        model = Comment
        fields = ('content', )
        widgets = {
            'content': COMMENT_WIDGET,
        }
