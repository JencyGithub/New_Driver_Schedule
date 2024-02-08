# admin_panel/urls.py
from django.urls import path
from . import views


app_name = 'frontend_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('notfound/', views.notfound, name='notfound'),
    # path('team/', views.team, name='team'),
    path('SignUp/', views.SignUp, name='SignUp'),
    # path('signup_save/', views.signup_save, name='signup_save'),
    path('career/', views.career, name='career'),
    # path('job_opening_form/<int:job_id>/', views.job_opening_form, name='job_opening_form'),
    # path('get_job_form/', views.get_job_form, name='get_job_form'),

    # Add more URLs for other custom admin panel views as needed
]