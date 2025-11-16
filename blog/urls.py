from django.urls import path
from . import views

urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog-list'),
    path('create/', views.BlogCreateView.as_view(), name='blog-create'),
    path('<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('posts/<int:post_id>/like/', views.like_post, name='like-post'),
    path('comments/<int:comment_id>/like/', views.like_comment, name='like-comment'),
]