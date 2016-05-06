from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from forms import YubikeyForm
from django.template import RequestContext


@login_required(login_url='/user/login')
def profile(request, template_name='cloudmesh_portal/layout/index.html'):
    username = request.user.username
    context = {
        'username': username
    }
    return render_to_response(template_name, context=context)


@login_required(login_url='/user/login')
def user_profile(request):
    profile = request.user.get_profile()
    return render_to_response(profile)


@login_required(login_url='/user/login')
def add_yubikey(request, template_name='cloudmesh_portal/users/yubikey.html',
                redirect_field_name=REDIRECT_FIELD_NAME):
    username = request.user.username
    redirect_to = template_name
    if request.method == 'POST':
        form = YubikeyForm(data=request.POST)
        if form.is_valid():
            pass
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
