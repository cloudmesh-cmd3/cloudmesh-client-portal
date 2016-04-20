from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response


@login_required(login_url='/user/login')
def profile(request, template_name='cloudmesh_portal/layout/index.html',
            redirect_field_name=REDIRECT_FIELD_NAME):
    return render_to_response(template_name)
