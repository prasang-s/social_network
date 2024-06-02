from django.urls import path
from users import views


urlpatterns = [
    path('signup/', views.UserSignUpAPIView().as_view()),
    path('signin/', views.UserSignInAPIView().as_view()),
    path('', views.SearchUsersAPIView().as_view()),
]
