from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='blog'),
    path('posts/', views.PostsView.as_view(), name='blog-posts'),
    path('posts/<slug:slug>/', views.PostView.as_view(), name='blog-post'),
    path('read-later/', views.ReadLaterView.as_view(), name='read-later'),
]
