from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True


class Patient(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients')
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=[('male','Male'),('female','Female'),('other','Other')])


    def __str__(self):
        return self.name


class Doctor(TimeStampedModel):
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    specialty = models.CharField(max_length=120)
    years_experience = models.PositiveIntegerField(default=0)


    def __str__(self):
        return f"Dr. {self.name} ({self.specialty})"


class PatientDoctor(TimeStampedModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='mappings')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='mappings')


    class Meta:
        unique_together = ('patient', 'doctor')


    def __str__(self):
        return f"{self.patient} ↔ {self.doctor}"