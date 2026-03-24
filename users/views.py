from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import UserLoginForm, UserRegistrationForm, UserUpdateForm


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('login')
    success_message = 'Пользователь успешно зарегистрирован'


class UserUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
    ):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:list')
    success_message = 'Пользователь успешно изменен'

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для изменения')
        return redirect('users:list')


class UserDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView
    ):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:list')
    success_message = 'Пользователь успешно удален'

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для удаления')
        return redirect('users:list')
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if (self.object.tasks_author.exists() or 
            self.object.tasks_executor.exists()):
            messages.info(
                request,
                'Невозможно удалить пользователя, связанного с задачами'
                )
            return redirect('users:list')
        return super().post(request, *args, **kwargs)


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    next_page = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Вы залогинены')
        return response


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, 'Вы разлогинены')
        return response