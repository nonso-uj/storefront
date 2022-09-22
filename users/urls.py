from django.urls import path
from knox import views as knox_views
from . import views

urlpatterns = [
    path('login/', views.login_view),
    path('login-api/', views.login_api),
    path('data-api/', views.get_user_data),
    path('register-api/', views.register_api),
    path('update-api/', views.update_api),
    path('logout/', knox_views.LogoutView.as_view()),
]

