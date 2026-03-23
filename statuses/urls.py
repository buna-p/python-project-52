from django.urls import path

from . import views

app_name = 'statuses'

urlpatterns = [
    path('', views.StatusListView.as_view(), name='list'),
    path('create/', views.StatusCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.StatusUpdateView.as_view(), name='update'),  # noqa: E501
    path('<int:pk>/delete/', views.StatusDeleteView.as_view(), name='delete'),  # noqa: E501
]