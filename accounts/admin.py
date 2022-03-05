from django.contrib import admin
from accounts.models import UserAccount, Profile


class UserAccountAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'created',
                    'is_active', 'is_admin', 'is_superuser', 'is_staff']
    exclude = ("password ",)
    readonly_fields = ('password', )


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'websiteUrl', 'short_bio', 'twitterUrl',
                    'facebookUrl', 'linkedInUrl', 'youtubeUrl', 'created', 'last_login']
    # prepopulated_fields = {'slug': ('categoryname',)}


# Register your models here.
admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(Profile, UserProfileAdmin)
