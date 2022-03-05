from django.shortcuts import render, redirect, get_object_or_404
from photos.models import Photos, Category
from accounts.models import Profile
from photos.forms import NewPhotoForm, EditPhotoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
from django.db.models import Q
from django.conf import settings
from django.views.decorators.http import require_POST


def Index(request):
    user = request.user
    categorys = Category.objects.all().order_by('?')
    photos = Photos.objects.filter(status="public").order_by('?')

    context = {
        'categorys': categorys,
        'photos': photos,
    }
    return render(request, "photo/index.html", context)


def Categories(request):
    categories = Category.objects.all().order_by('?')

    context = {
        "categories": categories
    }
    return render(request, 'photo/categories.html', context)


def photoCategory(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    photos = Photos.objects.filter(category=category).order_by('-created')

    context = {
        "category": category,
        "photos": photos
    }
    return render(request, "photo/photoCategory.html", context)


@login_required(login_url='accounts:login')
def NewPhoto(request):
    user = request.user
    categorys = Category.objects.all()
    title = "newphoto"

    if request.method == 'POST':
        form = NewPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get('image')
            title = form.cleaned_data.get('title')
            cameraType = form.cleaned_data.get('cameraType')
            location = form.cleaned_data.get('location')
            category = form.cleaned_data.get('category')
            status = form.cleaned_data.get('status')
            Photos.objects.create(image=image, title=title, cameraType=cameraType,
                                  location=location, category=category, status=status, user=user)
            messages.success(request, f'New photo added successfully')
            return redirect('photos:newPhoto')
    else:
        form = NewPhotoForm()

    context = {
        'form': form,
        'categorys': categorys,
        "title": title,
    }

    return render(request, 'photo/newPhoto.html', context)


@login_required(login_url='accounts:login')
def DeletePhoto(request, photo_id):
    user = request.user
    photo = get_object_or_404(Photos, id=photo_id)

    if user != photo.user:
        return HttpResponseForbidden
    else:
        photo.delete()
        messages.success(request, f'Photo deleted successfully')
    return redirect('photos:index')


@login_required(login_url='accounts:login')
def EditPhoto(request, photo_id):
    user = request.user
    photo = get_object_or_404(Photos, id=photo_id)

    if user != photo.user:
        return HttpResponseForbidden
    else:
        if request.method == 'POST':
            form = EditPhotoForm(request.POST, request.FILES, instance=photo)

            if form.is_valid():
                photo.image = form.cleaned_data.get('image')
                photo.title = form.cleaned_data.get('title')
                photo.category = form.cleaned_data.get('category')
                photo.save()
                messages.success(request, f'Photo updated successfully')
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            form = EditPhotoForm(instance=photo)

    context = {
        "form": form,
        "photo": photo
    }
    return render(request, 'photo/editphoto.html', context)


def photoDetail(request, photo_id):
    user = request.user
    photo = get_object_or_404(photo, id=photo_id)
    photographerMode = False
    title = photo

    if user == photo.user:
        teacherMode = True

    context = {
        "photo": photo,
        "photographerMode": photographerMode,
        "title": title,
    }
    return render(request, 'photo/photoDetail.html', context)


@login_required(login_url='accounts:login')
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Photos.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'error'})

def category(request):
    category = Category.objects.exclude(name='Default')
    context = {
        'category':category,
    }
    return context