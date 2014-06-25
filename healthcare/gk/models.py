"""
Models from template on genmymodel, with updates
"""
from django.db import models
import datetime

# Create your models here.



class Caregiver(models.Model):
    """
    to get the goals, use caregiver.goal_set
    to get the patients, use caregiver.patient_set
    to get the actions, use caregiver.action_set
    """
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=25)
    def __unicode__(self):
        return self.name

class Patient(models.Model):
    """
    to get goals, use patient.goal_set
    """
    name = models.CharField(max_length=100)
    caregiver = models.ManyToManyField(Caregiver)
    def __unicode__(self):
        return self.name


class Goal(models.Model):
    """
    to get the status updates, use goal.status_update_set
    """
    name = models.CharField(max_length=100)
    caregiver = models.ForeignKey(Caregiver)
    patient = models.ForeignKey(Patient)
    notes = models.TextField()
    active = models.BooleanField()
    def __unicode__(self):
        return self.name

'''
class StatusUpdateType(models.Model):
    name = models.CharField(max_length = 100)
    patient = models.ForeignKey(Patient)
    goal = models.ForeignKey(Goal)
    frequency = models.IntegerField()       # how is it defined?
    value_options = models.CharField(max_length = 100)
'''

class StatusUpdate(models.Model):
    #ctype = models.ForeignKey(StatusUpdateType)
    goal = models.ForeignKey(Goal)
    #date = models.DateField()
    pub_time = models.DateTimeField()
    data_value = models.IntegerField()
    reporting_caregiver = models.ForeignKey(Caregiver)
    notes = models.TextField()
    status = models.CharField(max_length = 100)
    def __unicode__(self):
        return self.notes

'''         will fall under caregiver / contact category if necessary
class FamilyMember(models.Model):
    name = models.CharField(max_length=100)
    patient = models.ForeignKey(Patient)
'''

class Action(models.Model):
    goal = models.ForeignKey(Goal)
    completed = models.BooleanField()
    name = models.CharField(max_length=100)
    notes = models.TextField()      #possibly unnecessary?
    caregiver = models.ForeignKey(Caregiver)
    deadline = models.DateField()
    def __unicode__(self):
        return self.name
    
