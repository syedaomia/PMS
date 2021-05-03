from django.urls import path
from .views import *


urlpatterns = [
   path('', user_login, name='user_login'),
   path('option', option, name='option'),
   path('patient-list', patient_list, name='patient_list'),
   path('add-patient', add_patient, name='add_patient'),
   path('user-logout', user_logout, name='user_logout'),
   path('history/<int:id>', history, name='history'),
   path('dashboard/<int:id>',dashboard, name='dashboard'),
   path('sprange/<int:id>',sprange, name='sprange'),
   path('patient-page',patient_page,name="patient_page"),
   path('patinfo',patinfo,name="patinfo")
   # path('rangraph/<int:id>',rangraph, name='rangraph'),
]
