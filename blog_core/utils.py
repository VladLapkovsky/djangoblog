"""This module provides custom mixins for the blog_core app.

Mixins:
DataMixin - could be used to add common arguments to all inherited classes.
FormStyleClassMixin - add CONTENT_AREA_CLASS to all inherited classes.
"""

from django import forms
from rest_framework import serializers

from users.models import CustomUser


class DataMixin:
    """Provide additional logic to all inherited classes."""

    def get_user_context(self, **kwargs: dict) -> dict:
        """Could be used to add common arguments to all inherited classes.

        Args:
            **kwargs: context kwargs

        Returns:
            kwargs
        """
        return kwargs


CONTENT_AREA_CLASS = 'form-control'


class FormStyleClassMixin(forms.Form):
    """Provide constructor to all inherited classes."""

    def __init__(self, *args: tuple, **kwargs: dict):
        """Add common widget class to all inherited classes.

        Args:
            *args: constructor args
            **kwargs: constructor kwargs
        """
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = CONTENT_AREA_CLASS


class APIPostMixin(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', write_only=True, queryset=CustomUser.objects.all())
