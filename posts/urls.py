from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<uuid:pk>/', views.post_detail, name='post_detail'),
]
