from django import forms
from django.core.exceptions import ValidationError

from blog_core.models import Post

CONTENT_AREA_CLASS = 'form-control'
TITLE_WIDGET = forms.TextInput(
    attrs={
        'placeholder': 'Title example',
    },
)
SLUG_WIDGET = forms.TextInput(
    attrs={
        'placeholder': 'your-post-url',
    },
)
CONTENT_WIDGET = forms.Textarea(
    attrs={
        'placeholder': 'Hello world!',
    },
)


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = CONTENT_AREA_CLASS

    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'author']
        widgets = {
            'title': TITLE_WIDGET,
            'slug': SLUG_WIDGET,
            'content': CONTENT_WIDGET,
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('The title is longer than 200 characters')
        return title
