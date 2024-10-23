from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.comment_list, name='comment_list'),
    path("auth/login/", LoginView.as_view
         (template_name="posts/LoginPage.html"), name="login-user"),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),
    path('get_comments/<uuid:premise_id>/', views.get_comments, name='get_comments'),

]
