from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.root),
    path('signin',views.signin),
    path('registration', views.registration),
    path('login', views.login),
    path('logout/',views.logout),
    path('patients/',views.patients),
    path('account/',views.account),
    path('payments/',views.payments),
    path('appointment_validate', views.appointment_validate, name='appointment_validate'),
    path('patient_validate', views.patient_validate),
    path('show_one_clinic',views.show_one_clinic),
    path('patients/delete/<int:id>',views.delete_patient),
    path('payments/delete/<int:id>',views.delete_payment),
    path('payments/edit/<int:payment_id>',views.edit_payment),
    path('showpatients/<int:cid>',views.showpatients),
    path('showpatients/all',views.showpatientsall),
    path('patient/<int:id>',views.patient),
    path('patient/update/<int:id>',views.update_patient),
    path('payment_validate', views.payment_validate),
    path('delete_appointment/<int:id>',views.delete_appointment),
    path('search-patients',csrf_exempt(views.search_patients),name="search-patients"),
    path('admin/',views.admin),
    path('admin/admin_dash',views.admin_dash),
    path('dashboard/', views.show_dashboard),
    path('search-payments',csrf_exempt(views.search_payments),name="search-payments"),
    path('payments/details/<int:id>',views.payment_details),
    path('add_clinic', views.add_clinic),

    

]