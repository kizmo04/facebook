from django.contrib.auth.models import AbstractUser
from django.db import models


# class MyUserManager(UserManager):
#     def create_facebook_user(
#             self,
#             social_id,
#             user_type,
#             email=None,
#             password=None,
#             **extra_fields):
#         extra_username = get_random_string(10)
#
#         return super().create_user(
#             username='{}{}'.format(username, extra_username),
#             social_id=social_id,
#             email=email,
#             password=password,
#             **extra_fields
#         )


class MyUser(AbstractUser):
    img_profile = models.ImageField(upload_to='user', blank=True)

    # CHOICES_USER_TYPE = (
    #     ('django', 'Django'),
    #     ('facebook', 'Facebook'),
    # )
    # social_id = models.CharField(max_length=100, blank=True)
    # user_type = models.CharField(
    #     max_length=15,
    #     choices=CHOICES_USER_TYPE,
    #     default=CHOICES_USER_TYPE[0][0]
    # )
    def __str__(self):
        return '{}{}'.format(
            self.first_name,
            self.last_name)
