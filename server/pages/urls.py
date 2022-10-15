from django.urls import path

from .views import homePageView, addView, mailView, profileView, chatView, addPostView

urlpatterns = [
    path('', homePageView, name='home'),
    path('add/', addView, name='add'),
    path('mail/', mailView, name='mail'),
    path('mail', mailView, name='mail'),
    path('chat', chatView, name='chat'),
    path('publishPost/', addPostView, name='publishPost'),
    path('profile/<int:uid>', profileView, name="profile")
]
