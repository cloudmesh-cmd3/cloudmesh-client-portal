from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from forms import RegisterForm, LoginForm, YubikeyForm
from django.contrib.auth.models import User
from models import PortalUser
from django.views.decorators.cache import never_cache
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login


# Ask for the user password after the token
YUBIKEY_USE_PASSWORD = getattr(settings, 'YUBICO_USE_PASSWORD', False)


# Name of the session key which stores user id
YUBIKEY_SESSION_USER_ID = getattr(settings, 'YUBICO_SESSION_USER_ID',
                                  'yubicodjango_user_id')


# Name of the session key which stores the name of the backend user used to log
# in.
YUBIKEY_SESSION_AUTH_BACKEND = getattr(settings, 'YUBICO_SESSION_AUTH_BACKEND',
                                       'yubicodjango_auth_backend')


# Name of the session key which stores attempt counter
YUBIKEY_SESSION_ATTEMPT_COUNTER = getattr(settings,
                                          'YUBIKEY_SESSION_ATTEMPT_COUNTER',
                                          'yubicodjango_counter')


# Django Yubico session keys
SESSION_KEYS = [YUBIKEY_SESSION_USER_ID, YUBIKEY_SESSION_AUTH_BACKEND,
                YUBIKEY_SESSION_ATTEMPT_COUNTER]


@never_cache
def register(request, template_name='cloudmesh_portal/users/register.html',
             redirect_field_name=REDIRECT_FIELD_NAME):
    redirect_to = settings.LOGIN_REDIRECT_URL
    if request.user.is_authenticated():
        return HttpResponseRedirect(redirect_to)
    if request.method == 'POST':
        # POST request to send form
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            print form.username
            # TODO add validation error if user is already there.
            user = User.objects.create_user(form.cleaned_data['username'],
                                            form.cleaned_data['email'],
                                            form.cleaned_data['password'])
            user.last_name = form.cleaned_data['lastname']
            user.first_name = form.cleaned_data['firstname']
            user.save()
            p = PortalUser(user=user, address=form.cleaned_data['address'],
                           additional_info=form.cleaned_data['additional_info'],
                           citizen=form.cleaned_data['citizen'],
                           country=form.cleaned_data['country'])
            p.save()
        else:
            # Not a valid form, open Register form with an error message.
            form = RegisterForm()
    else:
        # GET request to get form
        form = RegisterForm()

    dictionary = {'form': form, redirect_field_name: redirect_to}
    return render_to_response(template_name, dictionary,
                              context_instance=RequestContext(request))


@never_cache
def login(request, template_name='cloudmesh_portal/users/login.html',
             redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = settings.LOGIN_REDIRECT_URL
    if request.user.is_authenticated():
        return HttpResponseRedirect(redirect_to)

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.user

            if user is not None:
                if user.is_active:
                    # Check for yubikey user or not and then redirect to that.
                    auth_login(request, user)
                    return HttpResponseRedirect(redirect_to)
                else:
                    # Send back to login page with
                    return HttpResponseRedirect( reverse(
                        'yubico_django_password'))
            else:
                form = LoginForm()
        else:
            form = LoginForm()
    else:
        form = LoginForm()

    dictionary = {'form': form, redirect_field_name: redirect_to}

    return render_to_response(template_name, dictionary,
                              context_instance=RequestContext(request))


@never_cache
def yubi_otp(request, template_name='cloudmesh_portal/users/password.html',
             redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Displays the OTP form and handles the login action.
    """
    redirect_to = settings.LOGIN_REDIRECT_URL
    if request.method == 'POST':
        form = YubikeyForm(data=request.POST)
        if form.is_valid():
            pass
    else:
        form = YubikeyForm()

    dictionary = {'form': form, redirect_field_name: redirect_to}
    return render_to_response(template_name, dictionary,
                              context_instance=RequestContext(request))


@never_cache
def logout(request, next_page='/user/login',
           template_name='cloudmesh_portal/users/logout.html',
           redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Displays the Logout Message.
    """
    auth_logout(request)
    return HttpResponseRedirect(next_page)
