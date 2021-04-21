from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class PatientProfile(models.Model):
    
    first_name = models.CharField(max_length=300,blank=True, null=True)
    last_name = models.CharField(max_length=300,blank=True, null=True)
    age = models.CharField(max_length=300,blank=True, null=True )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,blank=True, null=True)



    address = models.CharField(max_length=300,blank=True, null=True)

    

    def __str__(self):
        return str(self.first_name)