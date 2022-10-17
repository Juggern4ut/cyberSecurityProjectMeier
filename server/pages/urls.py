from django.urls import path

from .views import homePageView, addChatView, mailView, profileView, chatView, addPostView, imageView, addFileView

urlpatterns = [
    path('', homePageView, name='home'),
    path('addChat/', addChatView, name='addChat'),
    path('mail/', mailView, name='mail'),
    path('mail', mailView, name='mail'),
    path('chat/<int:uid>', chatView, name='chat'),
    path('publishPost/', addPostView, name='publishPost'),
    path('profile/<int:uid>', profileView, name="profile"),
    path('image/<int:fileid>', imageView, name="imageView"),
    path('addImage/', addFileView, name="addImageView")
]
