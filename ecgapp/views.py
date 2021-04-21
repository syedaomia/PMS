from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout

from .models import *

# Create your views here.


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('/option')

    return render(request, 'login.html')


def option(request):
    user = request.user
    context = {'user': user}
    return render(request, 'option.html', context)


def patient_list(request):
    patientlist = PatientProfile.objects.all()
    context = {'patientlist': patientlist}
    return render(request, 'patientlist.html', context)


def add_patient(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        age = request.POST['age']
        gender = request.POST['gender']
        address = request.POST['address']
        profile = PatientProfile.objects.create(
            first_name=first_name, last_name=last_name, age=age, gender=gender, address=address)

        message = "Successfully Added!!!"
        status = 'success'
        context = {'message': message, 'sts': status}
        return redirect('/patient-list')

    else:
        return render(request, 'addpatient.html')




def user_logout(request):
    logout(request)
    return redirect('/')


def dashboard(request):
    return render(request,'dashboard.html')