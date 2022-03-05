from django.contrib import admin
from photos.models import Photos, Category

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Photos)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'status',
                    'approved', 'featured', 'published', 'updated']
    list_filter = ['approved', 'published', 'updated']
    list_editable = ['featured', 'approved']
    prepopulated_fields = {'slug': ('title',)}
