from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Friends, Message, Mail, Post, File
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from ratelimit.decorators import ratelimit
from bs4 import BeautifulSoup
import sqlite3
import json


# This view simulates an external mail server receiving a stolen cookie
@csrf_exempt
def mailView(request):
    Mail.objects.create(content=request.body.decode('utf-8'))
    print(request.body.decode('utf-8'))
    return HttpResponse('')


@login_required
def imageView(request, fileid):

    f = File.objects.get(pk=fileid)

    # Flaw 4 :
    # Not checking if the user is allowed to see the image.
    # User could open url /image/1 to download the image with id 1
    # no matter if he or she is allowed to do so
    # : End of flaw 4

    # Fix for flaw 4 :
    # areFriends = Friends.objects.filter((Q(friend1=request.user) & Q(friend2=f.owner.id)) | (Q(friend2=request.user) & Q(friend1=f.owner.id)))
    # if areFriends.count() == 0 and request.user.id != f.owner.id:
    #   return redirect('/')
    # : End of fix

    filename = f.data.name.split('/')[-1]
    response = HttpResponse(f.data, content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


@login_required
# @ratelimit(method='POST', key='ip', rate='1/2s', block=True)
def addChatView(request):
    partnerId = request.POST.get('partnerid')
    target = User.objects.get(id=partnerId)

    # Flaw 2 :
    Message.objects.create(source=request.user, target=target,
                           content=request.POST.get('content'))
    # : End of flaw 2

    # Fix for flaw 2 :
    #soup = BeautifulSoup(request.POST.get('content'))
    #content = soup.get_text()
    # Message.objects.create(source=request.user, target=target,
    #                      content=content)
    # : End of fix
    return redirect('/chat/'+partnerId)


@login_required
# @ratelimit(method='POST', key='ip', rate='1/5s', block=True)
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
    posts = Post.objects.filter(author=uid)
    files = File.objects.filter(owner=uid)
    photos = [{'id': f.id, 'name': f.data.name.split('/')[-1]} for f in files]

    # Flaw 3 :
    # No check if the user is allowed to see the posts
    # : End of flaw 3

    # Fix for flaw 3 :
    # areFriends = Friends.objects.filter((Q(friend1=request.user) & Q(friend2=uid)) | (Q(friend2=request.user) & Q(friend1=uid)))
    # if areFriends.count() == 0:
    #   return redirect('/')
    # : End of fix

    return render(request, 'pages/profile.html', {"username": profile.username, 'posts': posts, "photos": photos})


@login_required
def addFileView(request):
    data = request.FILES.get('file')
    f = File(owner=request.user, data=data)
    f.save()
    return redirect('/')


@login_required
def homePageView(request):
    posts = Post.objects.filter(author=request.user)
    files = File.objects.filter(owner=request.user)

    friends = []
    if request.user.id == 1:
        friends.append(User.objects.get(id=3))
    elif request.user.id == 2:
        friends.append(User.objects.get(id=3))
    elif request.user.id == 3:
        friends.append(User.objects.get(id=1))
        friends.append(User.objects.get(id=2))

    photos = [{'id': f.id, 'name': f.data.name.split('/')[-1]} for f in files]
    return render(request, 'pages/index.html', {"posts": posts, "photos": photos, "friends": friends})


@login_required
def chatView(request, uid):
    partner = User.objects.get(id=uid)
    messages = Message.objects.filter(
        (Q(source=request.user) & Q(target=partner)) | (Q(target=request.user) & Q(source=partner)))
    return render(request, 'pages/chat.html', {'partner': partner, 'msgs': messages})
