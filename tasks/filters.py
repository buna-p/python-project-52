import django_filters
from django import forms
from .models import Task
from statuses.models import Status
from labels.models import Label
from django.contrib.auth.models import User


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label='Статус',
        empty_label='Выбрать',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label='Исполнитель',
        empty_label='Выбрать',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label='Метка',
        empty_label='Выбрать',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']