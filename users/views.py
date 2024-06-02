from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, filters

from utils.utils import CustomValidation
from .models import User
from .serializers import UserDetailsSerializer, UserSerializer


class UserSignUpAPIView(CreateAPIView):
    serializer_class = UserSerializer


class UserSignInAPIView(APIView):
    def post(self, request, **kwargs):
        try:
            email, password = request.data.get(
                'email'), request.data.get('password')

            # check if user exists
            user = User.objects.filter(email=email).first()
            assert user, 'User does not exist.'

            # check if password is correct
            is_password_correct = user.check_password(password)
            assert is_password_correct, 'Incorrect password.'

            # if user exists, create token
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status.HTTP_200_OK)
        except AssertionError as e:
            raise CustomValidation(e, status.HTTP_400_BAD_REQUEST)


class SearchUsersAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('email', 'first_name')
    serializer_class = UserDetailsSerializer
    pagination_class = PageNumberPagination
    queryset = User.objects.all()
