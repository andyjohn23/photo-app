from django.urls import path
from . import views

app_name = "photos"

urlpatterns = [
    path('', views.Index, name="index"),
    path('photo/create/', views.NewPhoto, name="newPhoto"),
    path('categories/photo/<category_slug>/', views.photoCategory, name="photoCategory"),
    path('photo/edit/<photo_id>/', views.EditPhoto, name="editPhoto"),
    path('photo/<photo_id>/', views.photoDetail, name="photoDetail"),
    path('photo/delete/<photo_id>/', views.DeletePhoto, name="deletePhoto"),
    path('categories/', views.Categories, name="categories"),
    path('like/', views.image_like, name='like'),
]
