from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='tarefas/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.home, name='home'),
    path('add', views.add, name='add'),
    path('toggle/<int:id>', views.toggle, name='toggle'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('clear-completed/', views.clear_completed, name='clear_completed'),
    path('register/', views.register, name='register'),
]