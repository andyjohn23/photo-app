from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from cloudinary.models import CloudinaryField
from django.urls import reverse
from django.db.models.signals import post_save
from django.template.defaultfilters import truncatechars

# Create your models here.


class ManagerAccount(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('users must have an emailaddress')
        if not username:
            raise ValueError('users must have a username')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )

        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=70, unique=True)
    username = models.CharField(max_length=70, unique=True)
    created = models.DateTimeField(default=timezone.now)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = ManagerAccount()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Profile(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    websiteUrl = models.URLField(max_length=1000, blank=True)
    twitterUrl = models.CharField(max_length=1000, blank=True)
    facebookUrl = models.CharField(max_length=1000, blank=True)
    linkedInUrl = models.CharField(max_length=1000, blank=True)
    youtubeUrl = models.CharField(max_length=1000, blank=True)
    bio = models.TextField(blank=True)
    profileImage = CloudinaryField('profileImage', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username)
    
    @property
    def short_bio(self):
        return truncatechars(self.bio, 35)

    class Meta:
        ordering = ('-created',)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=UserAccount)
post_save.connect(save_user_profile, sender=UserAccount)
