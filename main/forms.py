# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm
from django.utils.translation import ugettext, ugettext_lazy as _

# Custom error messages
errors = {'required': 'Dette feltet er påkrevd', 'invalid': 'Ulovlig verdi',
          'password_too_short': 'Passordet er for kort', 'password_incorrect': _('Feil passord')}

labels = {
    'username': 'Username',
    'old_username': 'Current username',
    'password1': 'Password',
    'password2': 'Confirm password',
    'email': 'Email',
    'old_password': 'Current password',
    'new_password1': 'New password',
    'new_password2': 'Confirm new password'
}


class LoginForm(forms.Form):
    """
    Login form class. Creates and handles the login form.
    """

    username = forms.CharField(max_length=255, required=False, error_messages=errors, label='Username',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(required=False, error_messages=errors, label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    def clean(self):
        """
        Override the form clean method.

        Provide custom error messages for form and fields

        :return:
        """
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if not username or not password:
            raise forms.ValidationError("Alle felt er påkrevd")
        else:
            user = authenticate(username=username, password=password)

            if not user:
                raise forms.ValidationError("Feil brukernavn eller passord")

        return self.cleaned_data

    def login(self, request):
        """
        Login method. Authenticate user using provided username and password.

        :param request:
        :return: User object
        """
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        return user


class UserCreateForm(UserCreationForm):
    """
    User creation form class. Creates and handles form for creating new users
    """

    def __init__(self, *args, **kwargs):
        """
        Override init method of djangos build-in UserCreationForm to disable help texts and set custom labels

        :param args: args
        :param kwargs: kwargs
        """
        if 'userid' in kwargs:
            self.userid = kwargs.pop('userid')
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].error_messages = errors
            self.fields[fieldname].required = False
            self.fields[fieldname].label = labels[fieldname]
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        """
        Override clean method to make custom validation and feedback

        :return: Cleaned data
        """

        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        # if User.objects.filter(username=username).exists():
        #     raise forms.ValidationError("Dette brukernavnet er allerede brukt")

        if User.objects.filter(email=email).exclude(pk=self.userid).exists():
            raise forms.ValidationError("Denne eposten er allerede knyttet til en konto")

        if not password2 and password1:
            raise forms.ValidationError("Passord må ha minst 8 tegn og må ha både tall og bokstaver")

        if not username or not email or not password1 or not password2:
            raise forms.ValidationError("Alle felt er påkrevd")
        elif password1 != password2:
            raise forms.ValidationError("Passordene var ikke like")

        return self.cleaned_data

    def save(self, commit=True):
        """
        Save form data to a user object.

        :param userid:
        :param commit: Whether or not the user object should be commited to database
        :return: The newly created user object
        """

        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

    def update(self, user_id):
        """
        Update the user insatance
        :param user_id: Primary key for instance of user to update
        :return: New user object
        """
        user = User.objects.get(pk=user_id)
        user.email = self.cleaned_data.get('email')
        user.username = self.cleaned_data.get('username')
        user.set_password(self.cleaned_data.get('password1'))

        user.save()

        return user

    class Meta:
        """
        Meta class. Use the user model to add username and email fields
        """
        model = User
        fields = ['username', 'email', 'id']


class UserChangeForm(forms.ModelForm):
    """
    Form for changing username or user email
    """
    old_username = forms.CharField(max_length=150, widget=forms.HiddenInput, label='')

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)

        for fieldname in self.fields:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].error_messages = errors
            self.fields[fieldname].required = False
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})

            if fieldname != 'old_username':
                self.fields[fieldname].label = labels[fieldname]

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if not email or not username:
            raise forms.ValidationError("Alle felt er påkrevd")

        if username != self.cleaned_data.get('old_username') and User.objects.filter(username=username).exists():
            raise forms.ValidationError("Dette brukernavnet er allerede brukt")

        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'email']


class PasswdChangeForm(PasswordChangeForm):
    """
    Form for changing password
    """
    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': _('Feil passord'),
        'password_too_short': _('Passordet er for kort')
    })

    def __init__(self, *args, **kwargs):
        super(PasswdChangeForm, self).__init__(*args, **kwargs)

        for fieldname in self.fields:
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})
            self.fields[fieldname].required = False
            self.fields[fieldname].label = labels[fieldname]

    def clean(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        if not new_password2 and not new_password1:
            raise forms.ValidationError("Passord må ha minst 8 tegn og må ha både tall og bokstaver")
        elif new_password1 and not new_password2:
            raise forms.ValidationError("Passordene var ikke like")

        return self.cleaned_data
