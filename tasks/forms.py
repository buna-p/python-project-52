from django import forms
from django.contrib.auth.models import User

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        labels = {
            'name': 'Имя',
            'description': 'Описание',
            'status': 'Статус',
            'executor': 'Исполнитель',
            'labels': 'Метки',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'description':
                field.widget.attrs['rows'] = 3
        self.fields['status'].empty_label = '---------'
        self.fields['executor'].empty_label = '---------'
        self.fields['labels'].widget.attrs['size'] = 5
        self.fields['labels'].widget.attrs['class'] = 'form-control'
        self.fields['executor'].queryset = User.objects.all()