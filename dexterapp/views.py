# from multiprocessing import context
# from sre_constants import SUCCESS
# from tabnanny import check
# from tkinter.tix import Tree
from django.shortcuts import render ,redirect
from .models import  Doctor , Clinic , Patient   ,Appointment   , Payment
from django.contrib import messages
import re
from datetime import datetime, date
import bcrypt
import json
from django.http import JsonResponse
from django.http import HttpResponse
key='1234567890!@#$%^&*()1234567890mkdsmdkjsfnvjdf54545454##@#$bdsdwq$#$#!1254p'

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')


def root (request):
    return render(request,'welcome.html')



def search_patients(request):
    if request.method == 'POST':
        search_str=json.loads(request.body).get('searchText')
        patients=Patient.objects.filter( first_name__istartswith=search_str)|Patient.objects.filter( last_name__istartswith=search_str)|Patient.objects.filter( national_id__istartswith=search_str)|Patient.objects.filter( phone__istartswith=search_str)|Patient.objects.filter( date_of_birth__istartswith=search_str)|Patient.objects.filter(updated_at__istartswith=search_str)
        data=patients.values()
        return JsonResponse(list(data), safe=False)

def search_payments(request):
    if request.method == 'POST':
        search_str=json.loads(request.body).get('searchText')
        payments=Payment.objects.filter( date__istartswith=search_str)|Payment.objects.filter( amount__istartswith=search_str)|Payment.objects.filter(method__istartswith=search_str)
        data=payments.values()
        return JsonResponse(list(data), safe=False)



def signin(request):
    return render(request,'login.html')

def registration(request):
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        phone=request.POST['phone']
        national_id=request.POST['national_id']
        desc=request.POST['desc']
        role=request.POST['role']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() 
        new_user=Doctor.objects.create(first_name=first_name,last_name=last_name,email=email,password=pw_hash,phone=phone,national_id=national_id,desc=desc,role=role)
        request.session['first_name'] = new_user.first_name
        request.session['last_name'] = new_user.last_name
        request.session['id'] = new_user.id
        return redirect('/dashboard')

def login(request):
    logged_user= Doctor.objects.filter(email=request.POST['email'])
    if logged_user:
        logged_user=logged_user[0]
    request.session['first_name']=logged_user.first_name
    request.session['id']=logged_user.id
    request.session['last_name']=logged_user.last_name
    request.session['role']=logged_user.role
    return redirect('/account')

def logout(request):
    request.session.delete()
    return redirect('/')


def patients(request):
    if 'id' not in request.session:
        return redirect("/")
    doctor = Doctor.objects.get(id = request.session['id'])
    context={
    
            'patients':Patient.objects.filter(doctor = doctor),
            'clinics': doctor.doctor_clinics.all(),
        }   

    return render(request,'all_patients.html',context)

def delete_patient(request,id):
    patient=Patient.objects.get(id=id)
    patient.delete()
    return redirect('/patients')

def showpatients(request,cid):
    clinic=Clinic.objects.get(id=cid)
    context={
    'patients':clinic.clinic_patients.all(),
    'clinics':Clinic.objects.all(),

    }
    return render(request,'clinic_patient.html',context)

def showpatientsall(request):
    context={
        'clinics':Clinic.clinic_patients.all(),  
    }
    return render(request,'clinic_patient.html',context)

def payments(request):
    if 'id' not in request.session:
        return redirect("/")
    doctor = Doctor.objects.get(id = request.session['id'])
    context={
             
            'payments':Payment.objects.filter(doctor = doctor),
            'clinics': Clinic.objects.filter(doctor = doctor),
        }  
  
    return render(request,'all_payments.html',context)

def edit_payment(request,payment_id):
    p = Payment.objects.get(id=payment_id)
    p.amount= request.POST['edited_amount'] 
    p.save()
    return redirect("/payments")

def delete_payment(request,id):
    payment=Payment.objects.get(id=id)
    payment.delete()
    return redirect('/payments')


def payment_details(request,id):
    
    context = {
        'payment': Payment.objects.get(id=id),
    }
    
    return render(request,'payment_details.html', context)

def patient(request, id):
    if 'id' not in request.session:
        return redirect("/")
    context={
        'patients':Patient.objects.get(id = id),
        'clinics':Clinic.objects.all(),
        }
    return render(request,'patient.html',context)

def update_patient(request, id):
    patient=Patient.objects.get(id=id)
    if request.POST["first_name"]:
        patient.first_name=request.POST["first_name"]
    if request.POST['last_name']:
        patient.last_name=request.POST['last_name']
    if request.POST['national_id']:
        patient.national_id=request.POST['national_id']
    if request.POST['gender']:
        patient.gender=request.POST['gender']
    if request.POST['email']:
        patient.email=request.POST['email']
    if request.POST['phone']:
        patient.phone=request.POST['phone']
    if request.POST['clinic']:
        patient.clinic.name=request.POST['clinic']
    if request.POST['desc']:
        patient.desc=request.POST['desc']
    patient.save()
    return redirect(f'/patient/{id}')

def admin(request):

    return render(request,'admin.html')

def admin_dash(request):
    if request.POST['admin_pass']==key:
        request.session['key']=key
        return redirect('/dashboard')
    else:
        return redirect('/')

def show_dashboard(request):
    if 'key' in request.session:
        return render(request,'registration.html')
    else:
        return redirect('/')


def account(request):
    if 'id' not in request.session:
        return redirect("/")
    doctor = Doctor.objects.get(id = request.session['id'])
    context = {
        'all_appointments': doctor.doctor_appoints.all(),
        'clinics': Clinic.objects.filter(doctor = doctor)
    }

    return render(request, 'main_account.html', context)


def show_one_clinic(request):
    if 'id' not in request.session:
        return redirect("/")
    ids=request.session['id']
    d=Doctor.objects.get(id=ids)
    request.session['allclinics']=d.doctor.all()
    request.session['patientsfordoctor']=d.patients.all()
    return redirect('/patients')

def Clinic_validation(request):
    check = Clinic.objects.filter(name = request.POST['name'])
    error = False

    if len(request.POST['name'])< 3:
        messages.error(request,'The clinic name must contain more than two charecters', extra_tags = 'clinic_name' )
        error = True

    if not NAME_REGEX.match(request.POST['name']):
        messages.error(request,'The linic name must contain only alpha characters', extra_tags = 'clinic_name')
        error = True

    if len(request.POST['address'])< 9:
        messages.error(request,'The clinic address must be more than 8 cherecters', extra_tags = 'clinic_address')
        error = True

    if error == True:
        return redirect('/')

    elif error == False:
        Clinic.objects.create(name = request.POST['name'], address = request.POST['adddress'])

        messages.success(request, 'You have a new clinic !!', extra_tags = 'clinic_s')
        
        return redirect('/')
# ______________________________________________________
def patient_validate(request):
    check = Patient.objects.filter(national_id = request.POST['national_id'])
    error = False


    if len(request.POST['first_name'])< 3:
        messages.error(request,'First name must at least contain two characters!', extra_tags = 'first_name' )
        error = True

    if not NAME_REGEX.match(request.POST['first_name']):
        messages.error(request,'First name field must contain Alpha characters', extra_tags = 'first_name')
        error = True

    if not NAME_REGEX.match(request.POST['last_name']):
        messages.error(request,'Last name field must contain alpha characters only', extra_tags = 'last_name')
        error = True

    if len(request.POST['last_name'])< 3:
        messages.error(request,'Last name must at least contain two characters', extra_tags = 'last_name')
        error = True
    if len(request.POST['national_id'])!=9:
        messages.error(request,'The national id must be 9 digits!!',extra_tags='national_id')
        error=True

    if len(request.POST['phone'])!=10:
         messages.error(request,'The phone number must be only 10 digits',extra_tags='phone')
         error=True   
    if not EMAIL_REGEX.match(request.POST['email']):
        messages.error(request,'Email format must matches the email patterns ', extra_tags = 'email')
        error = True
    if len(request.POST['desc'])>55:
         messages.error(request,"Description can't be more than 55 characters ", extra_tags = 'desc')
         error=True

    if  check:
        messages.error(request,'this patient already exist !! ',extra_tags='national_id')
        error=True

    if error == True:
        return redirect('/account/#add_patient')

    elif error == False:
        Patient.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], gender = request.POST['gender'],
                                national_id = request.POST['national_id'], email = request.POST['email'], phone = request.POST['phone'], desc = request.POST['desc'], date_of_birth = request.POST['date_of_birth']
                                ,clinic = Clinic.objects.get(id = request.POST['clinic']), doctor = Doctor.objects.get(id = request.session['id']))

        messages.success(request, 'You have added a new patient succesfully', extra_tags = 'added')       
        return redirect('/account/#add_patient')
# ______________________________________________________________________________
def appointment_validate(request):
    error = False
    if len(request.POST['national_id']) != 9 :
        messages.error(request,'Please enter a valid national id', extra_tags = 'a_id' )
        error = True

    if len(request.POST['start_time'])< 1:
        messages.error(request,'Please enter a start date', extra_tags = 'start_time' )
        error = True

    if len(request.POST['end_time'])< 1:
        messages.error(request,'Please enter an end date', extra_tags = 'end_time' )
        error = True
    
    if len(request.POST['note'])>55:
        messages.error(request,'Please enter the note with length less than 55 characters',extra_tags='appointment_note')
        error=True
    
    if error == True:
        return redirect('/account/#add_appointment')

    elif error == False:
        patient = Patient.objects.get(national_id = request.POST['national_id'])
        Appointment.objects.create(national_id = request.POST['national_id'], date = request.POST['date'], start_time = request.POST['start_time'], end_time = request.POST['end_time'], note = request.POST['note'], patient = patient, doctor = Doctor.objects.get(id = request.session['id']))
    
    return HttpResponse(f'You have added a new appointment succesfully for {patient.first_name} {patient.last_name}')

def delete_appointment(request,id):
    appoint=Appointment.objects.get(id=id)
    appoint.delete()
    return redirect('/account')

#ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
def payment_validate(request):
    error = False

    if int(request.POST['amount'])< 20:
        messages.error(request,'The minimum accepted amount is 20', extra_tags = 'amount' )
        error = True

    if len(request.POST['date'])< 1:
        messages.error(request,'Please enter a the date', extra_tags = 'datep' )
        error = True
    
    # if len(request.POST['method'])==0:
    #     messages.error(request,'Please Enter a correct methodes -enter -C- for credit or -M- for cash',extra_tags='methodp')
    if len(request.POST['national_id'])!=9:
        messages.error(request,'National id number must be nine numbers only',extra_tags='np')
        error=True   
    if error == True:
        return redirect('/account/#add_payment')

    elif error == False:

        Payment.objects.create(amount = request.POST['amount'], date = request.POST['date'], method = request.POST['method'], doctor = Doctor.objects.get(id = request.session['id']),  patient = Patient.objects.get(national_id = request.POST['national_id']))

        messages.success(request, 'You have added a new payment succesfully.Thank you!', extra_tags = 'payment_correct')
        
        return redirect('/account/#add_payment')

def add_clinic(request):
    
    Clinic.objects.create(name = request.POST['name'], address = request.POST['address'], doctor = Doctor.objects.get(email = request.POST['email']))

    return redirect('/dashboard')