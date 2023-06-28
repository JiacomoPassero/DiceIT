from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

def home(request):

    # Check if the user belongs to the "admin" group
    if request.user.groups.filter(name='artigiani').exists():
        ctx = {'artigiano' : True}
    else:
        # User is not in the "admin" group
        # Perform actions for non-admin users
        ctx = {'artigiano' : False}

    return render(request, template_name='home.html', context=ctx)

@login_required
def diventa_artigiano(request):

    if request.method == "POST":
        user = request.user
        Group.objects.get_or_create(name='artigiani')
        artigiani = Group.objects.get(name='artigiani')
        artigiani.user_set.add(user)
        ctx = { 'registrato' : True}
    else:
        ctx = { 'registrato' : False}

    return render(request, template_name='diventa_artigiano.html', context=ctx)