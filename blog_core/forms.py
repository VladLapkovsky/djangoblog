from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from blog_core.models import Comment, CustomUser, Post
from blog_core.utils import FormStyleClass

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


class AddPostForm(FormStyleClass, forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content',)
        widgets = {
            'title': TITLE_WIDGET,
            'content': CONTENT_WIDGET,
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if Post.objects.filter(title=title).exists():
            raise ValidationError('The post with this title is already exists. Try another one.')
        if len(title) > 200:
            raise ValidationError('The title is longer than 200 characters.')
        return title


class RegisterUserForm(FormStyleClass, UserCreationForm):
    captcha = CaptchaField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('The user with this name is already exists. Try another one.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('The user with this email is already exists. Try another one.')
        return email


class LoginUserForm(FormStyleClass, AuthenticationForm):
    pass


COMMENT_WIDGET = forms.Textarea(
    attrs={
        'placeholder': 'Leave your comment',
        'rows': 3,
    },
)


class CommentForm(FormStyleClass, forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )
        widgets = {
            'content': COMMENT_WIDGET,
        }
