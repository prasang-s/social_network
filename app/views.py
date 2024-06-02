from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, pagination
from rest_framework.exceptions import ValidationError

from app.throttlers import UserSendRequestThrottle
from users.models import User
from utils.utils import CustomValidation
from .serializers import CreateRequestSerializer, UserFriendsSerializer
from .models import UserToFriendMapping


class UserSendAcceptRejectRequestAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_throttles(self):
        action = self.kwargs.get('action')
        if action == 'send':
            self.throttle_classes = (UserSendRequestThrottle, )

        return super().get_throttles()

    def post(self, request, action):

        try:
            assert action in ('send', 'accept', 'reject'), 'Invalid action.'

            if action == 'send':
                # check if to_user exists
                to_user = request.data.get('to_user')
                assert to_user, "'to_user' is required to send the request."
                User.objects.get(pk=to_user)

                # create request record
                request.data.update({'from_user': request.user.pk})
                serializer = CreateRequestSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'message': 'Friend request sent.'}, status.HTTP_200_OK)
            elif action == 'accept' or action == 'reject':
                request_id = request.data.get('request_id')
                assert request_id, f"'request_id' is required for request to be {action}ed."
                obj = UserToFriendMapping.objects.get(pk=request_id)

                # check if request is really sent to the current user
                assert obj.to_user == request.user, 'Invalid request.'

                # check if request is in pending state
                assert obj.status == UserToFriendMapping.PENDING, 'Request already accepted/rejected.'

                obj.status = UserToFriendMapping.ACCEPTED if action == 'accept' else UserToFriendMapping.REJECTED
                obj.save()

                return Response({'message': f'Request {action}ed.'})
        except User.DoesNotExist:
            raise CustomValidation('User does not exist.',
                                   status.HTTP_404_NOT_FOUND)
        except UserToFriendMapping.DoesNotExist:
            raise CustomValidation('Request does not exist.',
                                   status.HTTP_404_NOT_FOUND)
        except AssertionError as e:
            raise CustomValidation(e, status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            if isinstance(e, ValidationError):
                raise e
            raise CustomValidation()


class UserFriendsAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = pagination.PageNumberPagination
    serializer_class = UserFriendsSerializer

    def get_queryset(self):
        qs = UserToFriendMapping.objects.\
            filter(status=UserToFriendMapping.ACCEPTED,
                   from_user=self.request.user)

        return qs


class UserPendingRequestsAPIView(UserFriendsAPIView):
    def get_queryset(self):
        qs = UserToFriendMapping.objects.\
            filter(status=UserToFriendMapping.PENDING,
                   from_user=self.request.user)

        return qs
