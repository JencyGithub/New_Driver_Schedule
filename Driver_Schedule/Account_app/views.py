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


def index(request):
    return render(request, 'Account/dashboard.html')

def getForm1(request):
    return render(request, 'Trip_details/Form1.html')

def getForm2(request):
    return render(request, 'Trip_details/Form2.html')