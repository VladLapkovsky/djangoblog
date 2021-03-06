"""This module provides custom mixins for the blog_core app.

Mixins:
DataMixin - could be used to add common arguments to all inherited classes.
FormStyleClassMixin - add CONTENT_AREA_CLASS to all inherited classes.
"""

from django import forms


class DataMixin:
    """Provide additional logic to all inherited classes."""

    def get_user_context(self, **kwargs: dict) -> dict:
        """Could be used to add common arguments to all inherited classes.

        Args:
            **kwargs: context kwargs

        Returns:
            kwargs
        """
        if self.request.GET.get('next'):
            kwargs['user_login_path'] = self.request.GET['next']
            kwargs['user_register_path'] = self.request.GET['next']
        else:
            kwargs['user_login_path'] = self.request.get_full_path()
            kwargs['user_register_path'] = self.request.get_full_path()
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
