from django.shortcuts import render,redirect
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
import shutil, os,tabula, requests, colorama, subprocess
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.contrib import messages
from django import forms
from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request,'index.html')

def loginCall(request):
    return render(request,'login.html') 

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)

@csrf_protect   
def loginCheck(request):
    form = LoginForm()
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                CurrentUser_ = request.user
                if CurrentUser_.groups.filter(name='Driver').exists():
                    request.session['user_type'] = 'Driver'
                    return redirect('index')
                    
                elif CurrentUser_.groups.filter(name='Accounts').exists():
                    request.session['user_type'] = 'Accounts'
                    return redirect('Account:index')
                else:
                    request.session['user_type'] = 'SuperUser'
                    return redirect('Account:index')
            else:
                message = 'Login failed!'
                return HttpResponse(message)
    

def CustomLogOut(request):
    logout(request)
    return redirect('index')


    
    # Check if the user is a member of the "driver" group
    is_driver = user.groups.filter(name='driver').exists()

    context = {
        'is_driver': is_driver,
    }

    return render(request, 'your_template.html', context)