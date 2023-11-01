from django.shortcuts import render


# Create your views here.

# ````````````````````````````````````
# Appointment

# ```````````````````````````````````

def appointmentForm(request):
    return render(request, 'Appointment/appointmentForm.html')

