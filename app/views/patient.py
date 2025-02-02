from django.shortcuts import render,redirect
from app.models import Patient,Appointment,Payment
import random

from django.contrib import messages

# from django.views import View


from django.contrib.auth.decorators import login_required


def patient_unique_number(name):
    name=name
    while(True):  
        uq=random.randint(1000,9999)
        uq=name+str(uq)
        try:
            n=Patient.objects.get(patient_id=uq)
        except:
            return uq


@login_required(login_url='signin')
def doctor_prescription(request,slug):
    appointment_data = Appointment.objects.get(appointment_id=slug)
    patient_data = Patient.objects.get(patient_ref=appointment_data)
    print(patient_data)
    context = {
        'patient_data':patient_data,
    }
    return render(request,'dasboard/doctor/prescription.html',context)


@login_required(login_url='signin')
def patient_form(request,slug):

    if request.method == 'POST':
        symptoms=request.POST['symptoms']
        suggestion_test=request.POST['test']
        advice=request.POST['advice']
        rx=request.POST['rx']
    
        appointment_id = slug
        
        id=Appointment.objects.get(appointment_id=appointment_id)
    
        try:
            data = Patient.objects.get(patient_ref=id)
            messages.success(request, 'Already Exist')
            return redirect('dasboard')

        except:
            user=id.appointment_ref
            id.status=True
            id.save()
            patient_id=patient_unique_number("pat")
            ab=Patient.objects.create(patient_ref=id,patient_id=patient_id,symptoms=symptoms,suggestion_test=suggestion_test,advice=advice,rx=rx)
            b=Payment.objects.create(user=user,payment_ref=ab,amount=500)
            messages.success(request, 'Saved Successfully')
            return redirect('dasboard')
    else:
        
        user=request.user
        doctor=user.first_name
        data=Appointment.objects.get(appointment_id=slug,doctor=doctor)
        context = {
            'data':data
        }
        return render(request,'dasboard/doctor/patient-form.html',context)

