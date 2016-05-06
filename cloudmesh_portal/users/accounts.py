from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from forms import YubikeyForm, ProfileForm
from django.template import RequestContext
from django_yubico.models import YubicoKey
from models import PortalUser


@login_required(login_url='/user/login')
def dashboard(request, template_name='cloudmesh_portal/layout/index.html'):
    username = request.user.username
    context = {
        'username': username
    }
    return render_to_response(template_name, context=context)


@login_required(login_url='/user/login')
def user_profile(request, template_name='cloudmesh_portal/users/profile.html'
                                , redirect_field_name = REDIRECT_FIELD_NAME):
    username = request.user.username
    redirect_to = template_name
    if PortalUser.objects.filter(user=request.user).exists():
        profile = PortalUser.objects.get(user=request.user)
    else:
        context = {
            'username': username
        }
        return render_to_response('cloudmesh_portal/layout/index.html',
                                  context=context)
    form = ProfileForm(request.POST or None, initial={'Email':
                                                          profile.user.email,
                                                      'Username':
        profile.user.username, 'Firstname': profile.user.first_name,
                                'Lastname': profile.user.last_name,
                                'Address': profile.address,
                                'Additional Info':
                                    profile.additional_info})
    if request.method == 'POST':
        form = ProfileForm(data=request.POST)
        if form.is_valid():
            pass
    dictionary = {'form': form, redirect_field_name: redirect_to, 'username':
        username}
    return render_to_response(template_name, dictionary,
                              context_instance=RequestContext(request))


@login_required(login_url='/user/login')
def add_yubikey(request, template_name='cloudmesh_portal/users/yubikey.html',
                redirect_field_name=REDIRECT_FIELD_NAME):
    username = request.user.username
    redirect_to = template_name
    if request.method == 'POST':
        form = YubikeyForm(data=request.POST)
        if form.is_valid():
            if not YubicoKey.objects.filter(device_id=form.cleaned_data[
                'device_id']).exists():
                ykey = YubicoKey(device_id=form.cleaned_data['device_id'],
                                    client_id=form.cleaned_data['client_id'],
                                    secret_key=form.cleaned_data['secret_key'],
                                    user=request.user,
                                    enabled=True)
                ykey.save()
    else:
        form = YubikeyForm()

    dictionary = {'form': form, redirect_field_name: redirect_to, 'username':
        username}
    return render_to_response(template_name, dictionary,
                              context_instance=RequestContext(request))


@login_required(login_url='/user/login')
def how_to(request, template_name='cloudmesh_portal/users/how_to.html'):
    username = request.user.username
    context = {
        'username': username
    }
    return render_to_response(template_name, context=context)
