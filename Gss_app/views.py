from django.shortcuts import render
from django.http import FileResponse, HttpResponse
# from JobListings.models import *
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.http import HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
import os
from django.contrib.auth.models import User


# Create your views here.
def show_jd(request, jd_file_name):
    file = 'static/jd' + jd_file_name
    try:
        with open(file, 'rb') as pdf_file:
            response = HttpResponse(
                pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline;filename=mypdf.pdf'
            return response
    except FileNotFoundError:
        return redirect('/notfound')

        # return HttpResponse('file_not_found.html')


def index(request):
    return render(request, 'frontend_design/index.html')


def about(request):
    return render(request, 'frontend_design/about.html')


def services(request):
    return render(request, 'frontend_design/services.html')


def contact(request):
    return render(request, 'frontend_design/contact.html')

def notfound(request):
    return render(request, 'frontend_design/404notfound.html')

# def team(request):
#     return render(request, 'frontend_design/team.html')


def SignUp(request):
    return render(request, 'frontend_design/SignUp.html')

def career(request):
    return render(request, 'frontend_design/career.html')


# @csrf_protect
# def signup_save(request):

#     username = request.POST.get('username')
#     email = request.POST.get('email')
#     password1 = request.POST.get('password1')
#     # return HttpResponse(password1)
#     # Use keyword arguments to create the user
#     user_ = User.objects.create(username=username, email=email, password=password1, is_staff=True)
    
#     # Note: You should hash the password before saving it to the database.
#     # You can use the set_password method to do that.
#     user_.set_password(password1)
    
#     user_.save()
    
#     return HttpResponse('Work')

    
    
