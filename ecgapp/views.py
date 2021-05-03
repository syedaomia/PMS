from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout

from .models import *
from .database_download import *
import numpy as np
from .utils import *


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
        print(id)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        image = request.POST['image']
        age = request.POST['age']
        gender = request.POST['gender']
        address = request.POST['address']
        profile = PatientProfile.objects.create(
            first_name=first_name, last_name=last_name, age=age, gender=gender, address=address,
            image=image)

        message = "Successfully Added!!!"
        status = 'success'
        context = {'message': message, 'sts': status}
        return redirect('/patient-list')

    else:
        return render(request, 'addpatient.html')


def user_logout(request):
    logout(request)
    return redirect('/')


def history(request, id):

    pp = PatientProfile.objects.get(id=id)
 
    context = {'pp': pp}
    return render(request, 'history.html', context)


def dashboard(request, id):

    ppp = PatientProfile.objects.get(id=id)
    print(ppp)

    user = request.user
    dr = User.objects.get(username=user)
    print(dr.id)

    doctor_id = "d1"
    patient_id = "p" + str(ppp)

    abs_path = "Doctors/" + doctor_id + "/Patients/" + patient_id
    value = get_values(abs_path)
    print(value)
    hr = value[1]
    hr = float(np.asarray(hr))

    sp = value[2]
    sp = float(np.asarray(sp))

    chart = get_plot(abs_path)

    context = {'ppp': ppp, "hr": hr, "sp": sp, 'chart': chart}

    return render(request, 'dashboard.html', context)


def sprange(request, id):
    tt = PatientProfile.objects.get(id=id)
    print(tt)
    context ={'tt':tt }
    return render(request, 'sprange.html', context)




def patient_page(request):
    return render(request,'patientpage.html')


def patinfo(request):
    return render(request,'patinfo.html')