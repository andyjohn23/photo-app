from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from cloudinary.models import CloudinaryField
import uuid
from django.utils.text import slugify

# Create your models here.


class Category(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="Title", db_index=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('categories', args=[self.slug])

    def __str__(self):
        return self.name


class Photos(models.Model):
    class PhotoObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status="public")

    options = (
        ('public', 'Public'),
        ('private', 'Private'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    title = models.CharField(max_length=255)
    image = CloudinaryField('photo')
    slug = models.SlugField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    status = models.CharField(max_length=60, choices=options, default="Public")
    cameraType = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    featured = models.BooleanField(default=None, blank=True, null=True)
    approved = models.BooleanField(default=None, blank=True, null=True)
    liked = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like', default=None, blank=True)
    like_count = models.BigIntegerField(default='0')
    objects = models.Manager()
    photoobjects = PhotoObjects()
    published = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-published",)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
