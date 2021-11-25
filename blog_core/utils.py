from django import forms


class DataMixin:
    def get_user_context(self, **kwargs):
        return kwargs


CONTENT_AREA_CLASS = 'form-control'


class FormStyleClass(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = CONTENT_AREA_CLASS
