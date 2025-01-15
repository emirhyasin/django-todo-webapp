from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('change_password/', views.change_password, name='change_password'),
    path('todo_delete/<int:pk>', views.todo_delete, name='todo_delete'),
    path('todo_complete/<int:todo_id>/', views.todo_complete, name='todo_complete'),
    path('completed_todos/', views.completed_todos, name='completed_todos'),
    path('weather/', views.weather, name='weather'),
]
