from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from accounts.views import (
    UserView, visited_user, follow_user, accept_follow, decline_follow, ChangePasswordView
)

urlpatterns = [
    path('login/', obtain_auth_token),
    path('user/', UserView.as_view()),

    path('profile/<str:pk>/', visited_user),
    
    path('follow/<str:pk>/', follow_user),
    path('follow_decline/<str:pk>/', decline_follow),
    path('follow_accept/<str:pk>/', accept_follow),

    path('change_password/', ChangePasswordView.as_view())
]
