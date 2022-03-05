from django import forms
from photos.models import Photos, Category
from cloudinary.forms import CloudinaryFileField


class RequiredFieldsModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RequiredFieldsModelForm, self).__init__(*args, **kwargs)
        for bound_field in self:
            if (
                hasattr(bound_field, "field") and
                bound_field.name in self.Meta.required_fields
            ):
                bound_field.field.widget.attrs["required"] = "required"


class NewPhotoForm(RequiredFieldsModelForm):
    image = CloudinaryFileField(required=True, options={
        'tags': "photo, image",
        'format': 'jpg',
        'crop': 'limit',
        'width': 640,
        'quality': 'auto:eco',
    },)
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'validate'}), required=True, max_length=60)
    cameraType = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'validate'}), required=False, max_length=60)
    location = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'validate'}), required=False, max_length=60)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    status = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'validate'}), required=False, max_length=60)

    class Meta:
        required_fields = ['title', 'category', ]
        model = Photos
        fields = ('image', 'title', 'cameraType',
                  'location', 'category', 'status',)
        exclude = ('featured',)


class EditPhotoForm(RequiredFieldsModelForm):
    CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
    )
    image = CloudinaryFileField(required=False, options={
        'tags': "photo, image",
        'format': 'jpg',
        'crop': 'limit',
        'width': 640,
        'quality': 'auto:eco',
    },)
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'validate'}), required=True, max_length=60)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    cameraType = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'validate'}), required=False, max_length=60)
    location = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'validate'}), required=False, max_length=60)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    status = forms.CharField(widget=forms.Select(choices=CHOICES))

    class Meta:
        required_fields = ['title', 'category', ]
        model = Photos
        fields = ('image', 'title', 'cameraType',
                  'location', 'category', 'status',)
        exclude = ('featured',)
