from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Country, State, City, Gender, ClientRegister_Model
import re

class RegistrationForm(UserCreationForm):
    # Username field
    username = forms.CharField(
        max_length=100,
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )

    # Email field
    email = forms.EmailField(
        max_length=254,
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )

    # Phone number field
    phone_number = forms.CharField(
        max_length=15,
        label='Phone Number',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )

    # Country field
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        empty_label="Select Country",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Country",
        required=True
    )

    # State field
    state = forms.ModelChoiceField(
        queryset=State.objects.none(),
        empty_label="Select State",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="State",
        required=True
    )

    # City field
    city = forms.ModelChoiceField(
        queryset=City.objects.none(),
        empty_label="Select City",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="City",
        required=True
    )

    # Address field
    address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address'}),
        label="Address"
    )

    # Gender field
    gender = forms.ModelChoiceField(
        queryset=Gender.objects.all(),
        empty_label="Select Gender",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Gender"
    )

    # Password fields
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        label="Confirm Password"
    )

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not phone:
            raise forms.ValidationError('Phone number must be provided.')

        if not re.match(r'^[0-9]+$', phone):
            raise forms.ValidationError('Phone number must only contain numbers.')

        return phone

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("The two password fields must match.")
        return password2

    def __init__(self, *args, **kwargs):
        country_id = kwargs.pop('country_id', None)
        state_id = kwargs.pop('state_id', None)
        super().__init__(*args, **kwargs)

        # Dynamically set the queryset for state and city
        if country_id:
            self.fields['state'].queryset = State.objects.filter(country_id=country_id)
        else:
            self.fields['state'].queryset = State.objects.none()

        if state_id:
            self.fields['city'].queryset = City.objects.filter(state_id=state_id)
        else:
            self.fields['city'].queryset = City.objects.none()

    class Meta:
        model = ClientRegister_Model
        fields = [
            'username', 'email', 'phone_number', 'address',
            'gender', 'country', 'state', 'city',
            'password1', 'password2'
        ]
