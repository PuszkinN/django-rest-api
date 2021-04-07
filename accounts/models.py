from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from django.conf import settings
import datetime
from datetime import date
from content.models import Movie

class User(AbstractBaseUser):
    email = models.EmailField(_('email address'), unique=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    paid_until = models.DateField(
        null=True,
        blank=True
    )

    def set_paid_until(self, date_or_timestamp):
        if isinstance(date_or_timestamp, int):
            paid_until = date.fromtimestamp(date_or_timestamp)
        elif isinstance(date_or_timestamp, str):
            paid_until = date.fromtimestamp(int(date_or_timestamp))
        else:
            paid_until = date_or_timestamp

        self.paid_until = paid_until
        self.save()

    def has_paid(self, current_date=datetime.date.today()):
        if self.paid_until is None:
            return False
        return current_date < self.paid_until

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    is_private = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    background_image = models.ImageField(upload_to='backgrounds/', blank=True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followers', blank=True)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='following', blank=True)
    favorite_movies = models.ManyToManyField(Movie, blank=True, related_name='favorite_movies')
    
    def __str__(self):
        return f'{self.user} Profile'
    
    def followers_count(self):
        return self.followers.all().count()

    def following_count(self):
        return self.following.all().count()


class FollowRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='request_sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='request_receiver')
    is_active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def accept(self):
        self.receiver.profile.followers.add(self.sender)
    
    def cancel(self):
        self.is_active = False
    
    def discard(self):
        self.is_active = False

