from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import LabelForm
from .models import Label


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/label_list.html'
    context_object_name = 'labels'
    login_url = reverse_lazy('login')


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('labels')
    success_message = 'Метка успешно создана'
    login_url = reverse_lazy('login')


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('labels')
    success_message = 'Метка успешно изменена'
    login_url = reverse_lazy('login')


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/label_confirm_delete.html'
    success_url = reverse_lazy('labels')
    success_message = 'Метка успешно удалена'
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.task_set.exists():
            messages.info(request, 'Невозможно удалить метку')
            return redirect('labels')
        return super().post(request, *args, **kwargs)
