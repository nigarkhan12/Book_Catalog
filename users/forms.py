from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm, UsernameField


# Sign Up Form
class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Username'}
    ), required=True, max_length=50)
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}
    ), required=True, max_length=50)
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'input', 'placeholder': 'Password 1'}),required=True)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput(
        attrs={'class': 'input', 'placeholder': 'Password 2'}),required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            ]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'input', 'autofocus': True}),
            'email': forms.EmailInput(attrs={'class': 'input', 'required': True, 'autofocus': True}),
                    }

    # Validating password
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password2'] != cd['password1']:
            raise ValidationError("Password don't match")

        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('This email has already registered with us.')
        return email



# Profile Form
class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            ]


# class LoginForm(AuthenticationForm):
#     username = UsernameField(
#         widget=forms.TextInput(attrs={'class': 'input', 'autofocus': True, 'placeholder': 'username'})
#     )
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'password'}))
