from django import forms

from django.contrib.auth.models import User

from .models import UserProfile, PanditProfile

class UserSignupForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, required=True)
    password2 = forms.CharField(max_length=64, required=True)
    location_name = forms.CharField(max_length=100, required=True)
    lat = forms.DecimalField()
    lng = forms.DecimalField()

    class Meta:
        model = User
        fields = (
            'username','first_name', 'last_name', 'email',\
            'password','password2', 'location_name', 'lat', 'lng')

    def clean_password2(self):
        if not self.cleaned_data['password'] == self.cleaned_data['password2']:
            raise forms.ValidationError("Passwords don't match")


