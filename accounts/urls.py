from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path('join/signup/', views.register, name="signup"),
    path('login/', views.login_user, name="login"),
    path('edit/', views.editProfile, name="accountSettings"),
    path('edit/photo/', views.editProfilePhoto, name="profilePhotoSettings"),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]
