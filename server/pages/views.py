from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Friends, Message, Mail, Post
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import sqlite3
import json


# This view simulates an external mail server receiving a stolen cookie
@csrf_exempt
def mailView(request):
    Mail.objects.create(content=request.body.decode('utf-8'))
    print(request.body.decode('utf-8'))
    return HttpResponse('')


@login_required
def addView(request):
    target = User.objects.get(username=request.POST.get('to'))
    Message.objects.create(source=request.user, target=target,
                           content=request.POST.get('content'))
    return redirect('/')


@login_required
def addPostView(request):
    # Flaw 1 :
    conn = sqlite3.connect('./server/db.sqlite3')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO pages_post (author_id, content) VALUES (%i, '%s')" % (request.user.id, request.POST.get('content')))
    conn.commit()
    # : End of flaw 1

    # Fix for flaw 1 :
    #Post.objects.create(author=request.user, content=request.POST.get('content'))
    # : End of fix
    return redirect('/')


@login_required
def profileView(request, uid):
    profile = User.objects.get(id=uid)
    return render(request, 'pages/profile.html', {"username": profile.username})


@login_required
def homePageView(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'pages/index.html', {"posts": posts})


@login_required
def chatView(request):
    messages = Message.objects.filter(
        Q(source=request.user) | Q(target=request.user))
    users = User.objects.exclude(pk=request.user.id)
    return render(request, 'pages/chat.html', {'msgs': messages, 'users': users})
