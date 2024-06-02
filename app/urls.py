from django.urls import path
from . import views

urlpatterns = [
    path('requests/pending/', views.UserPendingRequestsAPIView().as_view()),
    path('requests/<action>/', views.UserSendAcceptRejectRequestAPIView().as_view()),
    path('friends/', views.UserFriendsAPIView().as_view()),
]
