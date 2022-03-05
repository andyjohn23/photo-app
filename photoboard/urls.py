from django.contrib import admin
from django.urls import path, include
from accounts import views as auth_views
admin.site.site_header = "PHOTO-BOARD PORTAL"
admin.site.index_title = "PHOTO-BOARD ADMIN"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls', namespace="accounts")),
    path('', include('photos.urls', namespace="photos")),
    path('logout/', auth_views.logout_user, name='logout'),
    path('profile/<username>/', auth_views.userProfile, name='profile'),
]
