"""
Models from template on genmymodel
"""
from django.db import models

# Create your models here.


class Caregiver(models.Model):
    """
    to get the goals, use caregiver.goal_set
    to get the patients, use caregiver.patient_set
    to get the actions, use caregiver.action_set
    """
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)

class Patient(models.Model):
    """
    to get goals, use patient.goal_set
    """
    name = models.CharField(max_length=100)
    caregiver = models.ManyToManyField(Caregiver)

class Goal(models.Model):
    """
    to get the status updates, use goal.status_update_set
    """
    name = models.CharField(max_length=100)
    caregiver = models.ForeignKey(Caregiver)
    patient = models.ForeignKey(Patient)
    notes = models.TextField()
    active = models.BooleanField()

class StatusUpdateType(models.Model):
    name = models.CharField(max_length = 100)
    patient = models.ForeignKey(Patient)
    goal = models.ForeignKey(Goal)
    frequency = models.IntegerField()       # how is it defined?
    value_options = models.CharField(max_length = 100)

class StatusUpdate(models.Model):
    #ctype = models.ForeignKey(StatusUpdateType)
    goal = models.ForeignKey(Goal)
    time = models.DateField(auto_now_add=True)
    reporting_caregiver = models.ForeignKey(Caregiver)
    notes = models.TextField()
    status = models.CharField(max_length = 100)

class FamilyMember(models.Model):
    name = models.CharField(max_length=100)
    patient = models.ForeignKey(Patient)

class Action(models.Model):
    goal = models.ForeignKey(Goal)
    completed = models.BooleanField()
    name = models.CharField(max_length=100)
    notes = models.TextField()
    caregiver = models.ForeignKey(Caregiver)
    deadline = models.DateField()
    
