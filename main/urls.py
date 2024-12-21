from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Strona główna
    path('register/', views.register, name='register'),  # Rejestracja
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard
    path('schedule/', views.schedule, name='schedule'),  # Plan zajęć
    path('grades/', views.grades, name='grades'),  # Oceny
    path('logout/', LogoutView.as_view(), name='logout'),  # Wylogowanie (GET działa domyślnie)
]
