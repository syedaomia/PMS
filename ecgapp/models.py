from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import DateField
from datetime import datetime
import numpy as np




# Create your models here.
class OTP(models.Model):
    otp = models.CharField(max_length=300)
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return self.otp






class PatientProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=300,blank=True, null=True)
    last_name = models.CharField(max_length=300,blank=True, null=True)
    image =  models.ImageField(blank=True, null=True)
    id =  models.AutoField(primary_key=True)
    age = models.CharField(max_length=300,blank=True, null=True )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,blank=True, null=True)


 
    address = models.CharField(max_length=300,blank=True, null=True)
    
    
  


    def __str__(self):
        return (str(self.id))




