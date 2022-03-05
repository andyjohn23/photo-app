from django import forms
from accounts.models import UserAccount, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.forms.widgets import TextInput
from cloudinary.forms import CloudinaryFileField


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(
        max_length=200, help_text='Required valid emailaddress')

    class Meta:
        model = UserAccount
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = UserAccount.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f'Email {email} is already in use!')

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = UserAccount.objects.get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f'Username {username} is already in use!')


class AuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
        model = UserAccount
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Email or password is invalid!')


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(),
                               max_length=15, required=True)
    email = forms.CharField(widget=forms.TextInput(),
                            max_length=100, required=True)

    class Meta:
        model = UserAccount
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if not email.isdigit():
            users = UserAccount.objects.exclude(pk=self.instance.pk).filter(
                email__iexact=email
            ).exists()
            if users:
                raise forms.ValidationError("Email has already been taken by someone else")
        else:
            raise forms.ValidationError("Email can't contain only numbers")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username.isdigit():
            users = UserAccount.objects.exclude(pk=self.instance.pk).filter(
                username__iexact=username
            ).exists()
            if users:
                raise forms.ValidationError("Username has already been taken by someone else")
        else:
            raise forms.ValidationError("Username can't contain only numbers")
        return username


class ProfileUpdateForm(forms.ModelForm):
    facebookUrl=forms.CharField(widget = forms.TextInput(),
                            max_length = 100, required = False)
    linkedInUrl=forms.CharField(widget = forms.TextInput(),
                            max_length = 100, required = False)
    twitterUrl=forms.CharField(widget = forms.TextInput(),
                            max_length = 100, required = False)
    websiteUrl=forms.CharField(widget = forms.TextInput(),
                            max_length = 100, required = False)
    youtubeUrl=forms.CharField(widget = forms.TextInput(),
                            max_length = 100, required = False)
    bio=forms.CharField(widget = forms.Textarea(
        attrs={'class': 'input is-medium'}), max_length = 250, required = False)

    class Meta:
        model=Profile
        fields=['bio', 'facebookUrl', 'linkedInUrl',
            'twitterUrl', 'websiteUrl', 'youtubeUrl', ]

class ProfilePhotoUpdateForm(forms.ModelForm):
    profileImage = CloudinaryFileField(required=False, options={
        'tags': "users, profileImage",
        'format': 'jpg',
        'crop': 'limit',
        'width': 640,
        'quality': 'auto:eco',
    },)

    class Meta:
        model=Profile
        fields=['profileImage',]