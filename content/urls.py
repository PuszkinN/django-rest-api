from django.urls import path, include 
# from content.views import get_user_posts

from content.views import (
    MovieView,
    CommentView,
    CommentsList,
    LikeMovie,
    LikePhoto
)

urlpatterns = [
    # path('get_user_posts/<str:pk>/', get_user_posts),

    path('movie_create/', MovieView.as_view()),
    path('movie_delete/<str:pk>/', MovieView.as_view()),
    path('movie_detail/<str:pk>/', MovieView.as_view()),
    path('movie_update/<str:pk>/', MovieView.as_view()),

    path('get_post_comments/<str:pk>/', CommentsList.as_view()),
    path('create_comment/<str:pk>/', CommentView.as_view()),

    path('movie_like/<str:pk>/', LikeMovie.as_view()),
    path('photo_like/<str:pk>/', LikePhoto.as_view()) 
]
