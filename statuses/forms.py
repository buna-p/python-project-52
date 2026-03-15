from django import forms

from .models import Status


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        labels = {
            'name': 'Имя',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Имя статуса'})  # noqa: E501
