from rest_framework.throttling import UserRateThrottle


class UserSendRequestThrottle(UserRateThrottle):
    rate = '3/min'
