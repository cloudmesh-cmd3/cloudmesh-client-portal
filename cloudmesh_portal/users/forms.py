import re

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from models import PortalUser
from django_yubico.models import YubicoKey
from django.utils.translation import ugettext_lazy as _
from django_countries import countries
from django_countries.fields import LazyTypedChoiceField
from django.contrib.auth import authenticate

RE_PUBLIC_ID = re.compile(r'^[cbdefghijklnrtuv]{12}$')
RE_TOKEN = re.compile(r'^[cbdefghijklnrtuv]{32,64}$')

# Multi mode (default = False)
YUBICO_MULTI_MODE = getattr(settings, 'YUBICO_MULTI_MODE', False)

# How many OTPs user needs to enter when multi mode is enabled
YUBICO_MULTI_NUMBER = getattr(settings, 'YUBICO_MULTI_NUMBER', 3)

STYLE = ''''background:url("/site_media/images/yubiright_16x16.gif") no-repeat
scroll 2px 2px white; padding-left:20px;'''
PASSWORD_INPUT_WIDGET_ATTRS = {'style': STYLE}


class RegisterForm(forms.Form):
    email = forms.EmailField(label=_('Email'),
                             widget=forms.EmailInput(),
                             required=True)
    username = forms.CharField(label=_('Username'),
                               required=True)
    firstname = forms.CharField(label=_('Firstname'),
                                required=True)
    lastname = forms.CharField(label=_('Lastname'),
                               required=True)
    password = forms.CharField(label=_('Password'),
                               widget=forms.PasswordInput(),
                               required=True)
    address = forms.CharField(label=_('Address'),
                              required=True)
    additional_info = forms.CharField(label=_('Additional Info'))
    country = LazyTypedChoiceField(label=_('Country'),
                                   choices=countries)
    citizen = LazyTypedChoiceField(label=_('Citizenship'),
                                   choices=countries)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.email = None
        self.username = None
        self.password = None
        self.firstname = None
        self.lastname = None
        self.address = None
        self.additional_info = None

    def clean(self):
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("That user is already taken")
        return username


class LoginForm(forms.Form):
    username = forms.CharField(label=_('Username'), required=True)
    password = forms.CharField(label=_('Password'),
                               widget=forms.PasswordInput(),
                               required=True)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user = authenticate(username=username, password=password)

        if self.user is None:
            raise forms.ValidationError(_('Invalid Credentials. Please '
                                          'Register.'))

        return self.cleaned_data


class YubikeyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(YubikeyForm, self).__init__(*args, **kwargs)

        min_length = 34
        max_length = 64

        if not YUBICO_MULTI_MODE:
            widget = forms.PasswordInput(attrs=PASSWORD_INPUT_WIDGET_ATTRS)
            self.fields['otp'] = forms.RegexField(label=_('OTP'),
                                                  widget=widget,
                                                  regex=RE_TOKEN,
                                                  min_length=min_length,
                                                  max_length=max_length)

    def clean(self):

        otp_list = []
        if not YUBICO_MULTI_MODE:
            otp = self.cleaned_data.get('otp')
            otp_list.append(otp)
        else:
            for index in range(0, YUBICO_MULTI_NUMBER):
                otp = self.cleaned_data.get('otp_%d' % index)
                otp_list.append(otp)

        return self.cleaned_data


class YubikeyForm(forms.Form):
    device_id = forms.CharField(max_length=12)
    client_id = forms.IntegerField()
    enabled = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        super(YubikeyForm, self).__init__(*args, **kwargs)

    class Meta:
        model = YubicoKey
        exclude = ('user', )

    def save(self, *args, **kwargs):
        u = self.instance.user
        yubi_form = super(YubikeyForm, self).save(*args, **kwargs)
        return yubi_form


class ProfileForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['active'].initial = self.instance.user.is_active
        except User.DoesNotExist:
            pass

    email = forms.EmailField(label="Primary email", help_text='')

    class Meta:
      model = PortalUser
      exclude = ('user',)

    def save(self, *args, **kwargs):
        """
        Update the primary email address on the related User object as well.
        """
        u = self.instance.user
        u.email = self.cleaned_data['email']
        u.save()
        profile = super(ProfileForm, self).save(*args,**kwargs)
        return profile
