from django.urls import path

from users import views

urlpatterns = [
    path('', views.UserListView.as_view(), name='users'),
    path('create/', views.UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/update/ ', views.UserUpdateView.as_view(), name='user_update'),  # noqa: E501
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),  # noqa: E501
]