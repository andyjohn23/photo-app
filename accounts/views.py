from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterUserForm, AuthenticationForm, ProfileUpdateForm, UserUpdateForm, ProfilePhotoUpdateForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from accounts.models import UserAccount, Profile
from photos.models import Photos, Category
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from django.template import loader
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.urls import resolve
from django.db.models import Q

# Create your views here.


@login_required(login_url='accounts:login')
def userProfile(request, username):
    user = get_object_or_404(UserAccount, username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name
    title = profile

    if url_name == 'profile':
        photos = Photos.objects.filter(Q(user=user)).distinct().order_by('-published')

    number_of_photos = Photos.objects.filter(Q(user=user)).count()

    template = loader.get_template('photo/profile.html')

    context = {
        'photos': photos,
        'profile': profile,
        'url_name': url_name,
        'number_of_photos': number_of_photos,
        'title': title
    }

    return HttpResponse(template.render(context, request))


@login_required(login_url='accounts:login')
def editProfile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Profile updated successfully')
            return redirect('accounts:accountSettings')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'photo/editProfile.html', context)


@login_required(login_url='accounts:login')
def editProfilePhoto(request):
    if request.method == 'POST':
        form = ProfilePhotoUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)

        if form.is_valid():
            form.save()
            messages.success(request, f'Profile Photo updated successfully')
            return redirect('accounts:profilePhotoSettings')

    else:
        form = ProfilePhotoUpdateForm(instance=request.user.profile)

    context = {
        'form': form,
    }

    return render(request, 'photo/editProfilePhoto.html', context)

def register(request, *arg, **kwargs):
    user = request.user

    if user.is_authenticated:
        return redirect('photos:index')
    context = {}

    if request.POST:
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            destination = get_redirect_if_exists(request)
            if destination:
                return redirect(destination)
            return redirect('photos:index')
        else:
            context['register_form'] = form

    return render(request, 'photo/signup.html', context)


def login_user(request, *args, **kwargs):

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('photos:index')

    destination = get_redirect_if_exists(request)
    if request.POST:
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                destination = get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)
                return redirect('photos:index')

        else:
            context['login_form'] = form

    return render(request, 'photo/login.html', context)


def logout_user(request, *args, **kwargs):
    logout(request)
    return redirect("photos:index")


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get('next'):
            redirect = str(request.GET.get('next'))

    return redirect

