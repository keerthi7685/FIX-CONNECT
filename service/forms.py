from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, VendorProfile, Appliance, Booking, Review, VideoConsultation


class CustomerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'First Name'
    }))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Last Name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-input', 'placeholder': 'Email Address'
    }))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Phone Number'
    }))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'City'
    }))
    area = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Area / Locality'
    }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'city', 'area', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Confirm Password'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'customer'
        if commit:
            user.save()
        return user


class VendorRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'First Name'
    }))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Last Name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-input', 'placeholder': 'Email Address'
    }))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Phone Number'
    }))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'City'
    }))
    area = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Area / Locality'
    }))
    business_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Business / Service Name'
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-input', 'placeholder': 'Describe your services...', 'rows': 3
    }), required=False)
    experience_years = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={
        'class': 'form-input', 'placeholder': 'Years of Experience'
    }))
    hourly_rate = forms.DecimalField(min_value=0, widget=forms.NumberInput(attrs={
        'class': 'form-input', 'placeholder': 'Hourly Rate (₹)'
    }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'city', 'area', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Confirm Password'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'vendor'
        if commit:
            user.save()
            VendorProfile.objects.create(
                user=user,
                business_name=self.cleaned_data['business_name'],
                description=self.cleaned_data.get('description', ''),
                experience_years=self.cleaned_data['experience_years'],
                hourly_rate=self.cleaned_data['hourly_rate'],
            )
        return user


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input', 'placeholder': 'Password'
    }))


class ApplianceForm(forms.ModelForm):
    class Meta:
        model = Appliance
        fields = ['appliance_type', 'brand', 'model_number', 'purchase_date', 'warranty_end_date', 'notes']
        widgets = {
            'appliance_type': forms.Select(attrs={'class': 'form-input'}),
            'brand': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Brand Name'}),
            'model_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Model Number'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'warranty_end_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Additional notes...'}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service', 'description', 'scheduled_date', 'scheduled_time', 'address']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Describe your issue...'}),
            'scheduled_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'scheduled_time': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'address': forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Service address...'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'max': 5, 'placeholder': 'Rating (1-5)'}),
            'comment': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Write your review...'}),
        }


class VendorProfileForm(forms.ModelForm):
    class Meta:
        model = VendorProfile
        fields = ['business_name', 'description', 'services', 'experience_years', 'hourly_rate', 'is_available']
        widgets = {
            'business_name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'services': forms.CheckboxSelectMultiple(),
            'experience_years': forms.NumberInput(attrs={'class': 'form-input'}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-input'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
