from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('', views.UserListView.as_view(), name='list'),
    path('create/', views.UserCreateView.as_view(), name='create'),
    path('<int:pk>/update/ ', views.UserUpdateView.as_view(), name='update'),  # noqa: E501
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='delete'),  # noqa: E501
]