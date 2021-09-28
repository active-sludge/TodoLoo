"""todoloo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todo import views


urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('signup/', views.sign_up_user, name='signupuser'),
    path('logout/', views.log_out_user, name='logoutuser'),
    path('login/', views.log_in_user, name='loginuser'),

    # Todos
    path('', views.home, name='home'),
    path('create/', views.create_todo, name='createtodo'),
    path('currenttodos/', views.current_todos, name='currenttodos'),
    path('completed/', views.completed_todos, name='completedtodos'),
    path('todo/<int:todo_pk>', views.todo_detail, name='todo'),
    path('todo/<int:todo_pk>/complete', views.complete_todo, name='completetodo'),
    path('todo/<int:todo_pk>/delete', views.delete_todo, name='deletetodo'),

    # Articles
    path('articles/', views.articles, name='articles'),
    path('refresh/', views.refresh_articles, name='refresharticles'),
    path('bookmark/<int:article_pk>/', views.bookmark, name='bookmark'),


]
