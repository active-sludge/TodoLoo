from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout,authenticate
from .forms import TodoForm
from .models import Todo, Article
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from . import pubmed_service


def sign_up_user(request):
    if request.method == "GET":
        return render(request, 'todo/signup.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password= request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signup.html',
                              {'form': UserCreationForm(), 'error': 'That user name has already has been taken. Please choose a new username.'})
        else:
            return render(request, 'todo/signup.html', {'form': UserCreationForm(), 'error':'Passwords did not match'})


@login_required
def current_todos(request):
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos': todos})

def articles(request):
    articles = Article.objects.all()
    return render(request, 'articles/article_list.html', {'articles': articles})

def refresh_articles(request):
    pubmed_service.get_articles_with_details()
    return redirect('articles')

@login_required
def bookmark(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    print(article)
    print('bookmarked')
    if article.todo:
        article.todo.delete()
    else:
        todo = Todo.objects.create(
            title = article.article_title,
            memo = article.article_abstract,
            user = request.user
        )
        todo.save()
        article.todo = todo
        article.save()

    return redirect('articles')

@login_required
def log_out_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def home(request):
    return render(request, 'todo/home.html')


def log_in_user(request):
    if request.method == "GET":
        return render(request, 'todo/login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if user is None:
            return render(request, 'todo/login.html', {'form': AuthenticationForm(), 'error': 'Username and password did not match.'})
        else:
            login(request, user)
            return redirect('currenttodos')


@login_required
def create_todo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form  = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html',
                          {'form': TodoForm(), 'error': 'Bad data entry. Try again.'})


@login_required
def todo_detail(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/todo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/todo.html', {'todo': todo, 'form': form, 'error':'Bad info.'})


@login_required
def complete_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.date_completed = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required
def delete_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')


@login_required
def completed_todos(request):
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')
    return render(request, 'todo/completedtodos.html', {'todos': todos})