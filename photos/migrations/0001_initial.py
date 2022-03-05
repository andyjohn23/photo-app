# Generated by Django 3.2.10 on 2022-03-05 13:00

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Title')),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('slug', models.SlugField(unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Photos',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='photo')),
                ('slug', models.SlugField(max_length=255)),
                ('status', models.CharField(choices=[('public', 'Public'), ('private', 'Private')], default='Public', max_length=60)),
                ('cameraType', models.CharField(blank=True, max_length=255, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('featured', models.BooleanField(blank=True, default=None, null=True)),
                ('approved', models.BooleanField(blank=True, default=None, null=True)),
                ('like_count', models.BigIntegerField(default='0')),
                ('published', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='photos.category')),
                ('liked', models.ManyToManyField(blank=True, default=None, related_name='like', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-published',),
            },
        ),
    ]
