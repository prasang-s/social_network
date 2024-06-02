from django.db import models
from users.models import User


class UserToFriendMapping(models.Model):
    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]

    to_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='friends')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.SmallIntegerField(blank=False, null=False, default=PENDING,
                                      choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        unique_together = [['to_user', 'from_user']]
