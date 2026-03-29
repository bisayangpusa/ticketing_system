from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from tickets import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('hotdog', admin.site.urls), # Ensure this is at the TOP
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('edit/<int:pk>/', views.edit_ticket, name='edit_ticket'),
]