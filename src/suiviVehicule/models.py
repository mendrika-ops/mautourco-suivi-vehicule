from datetime import date
import datetime

from django.db import models


# Create your models here.

class User(models.Model):
    id = models.indexes
    username = models.CharField(max_length=100)
    mail = models.EmailField(max_length=150)
    pswd = models.CharField(max_length=250)
    contact = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=100, null=True)
    sexe = models.CharField(max_length=20, null=True)
    description = models.TextField()
    etat = models.IntegerField()


class TrajetcoordonneeSamm(models.Model):
    vehicleno = models.CharField(max_length=100)
    driver_oname = models.CharField(max_length=150)
    driver_mobile_number = models.CharField(max_length=50)
    FromPlace = models.CharField(max_length=150)
    ToPlace = models.CharField(max_length=150)
    id_trip = models.IntegerField()
    trip_no = models.IntegerField()
    trip_start_date = models.CharField(max_length=15, null=False)
    pick_up_time = models.TimeField()
    PickUp_H_Pos = models.CharField(max_length=100)
    PickEnd_H_Pos = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True)
    duration = models.CharField(max_length=100, null=True)
    couleur = models.CharField(max_length=100, null=True)
    estimatetime = models.CharField(max_length=50,null=True)
    datetime = models.CharField(max_length=15, null=False)
    Uid = models.CharField(max_length=50, null=True)
    idstatusposdetail = models.IntegerField(null=True)
    trip_start_time = models.TimeField()
    idstatusparameter = models.IntegerField(null=True)
    class Meta:
        managed = False
        db_table = 'suiviVehicule_laststatuswithorder'


class Trajetcoordonnee(models.Model):
    vehicleno = models.CharField(max_length=100)
    driver_oname = models.CharField(max_length=150)
    driver_mobile_number = models.CharField(max_length=50)
    FromPlace = models.CharField(max_length=150)
    ToPlace = models.CharField(max_length=150)
    id_trip = models.IntegerField()
    trip_no = models.IntegerField()
    trip_start_date = models.CharField(max_length=15, null=False)
    pick_up_time = models.TimeField()
    PickUp_H_Pos = models.CharField(max_length=100)
    PickEnd_H_Pos = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True)
    duration = models.CharField(max_length=100, null=True)
    couleur = models.CharField(max_length=100, null=True)
    estimatetime = models.CharField(max_length=50, null=True)
    trip_start_time = models.TimeField()

class TrajetcoordonneeWithUid(models.Model):
    vehicleno = models.CharField(max_length=100)
    driver_oname = models.CharField(max_length=150)
    driver_mobile_number = models.CharField(max_length=50)
    FromPlace = models.CharField(max_length=150)
    ToPlace = models.CharField(max_length=150)
    id_trip = models.IntegerField()
    trip_no = models.IntegerField()
    trip_start_date = models.CharField(max_length=15, null=False)
    pick_up_time = models.TimeField()
    PickUp_H_Pos = models.CharField(max_length=100)
    Uid = models.CharField(max_length=50, null=True)
    class Meta:
        managed = False
        db_table = 'suiviVehicule_trajetcoordonneesummary'

class UidName(models.Model):
    vehicleno = models.CharField(max_length=100)
    Uid = models.CharField(max_length=50)
    coordonnee = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'UidName'
    def __init__(self, vehicleno, Uid, coordonnee):
        self.vehicleno = vehicleno
        self.Uid = Uid
        self.coordonnee = coordonnee

class Statuspos(models.Model):
    id = models.indexes
    datetime = models.DateTimeField()
    desc = models.CharField(max_length=100)


class Statusposdetail(models.Model):
    id = models.indexes
    idmere = models.ForeignKey(Statuspos, on_delete=models.CASCADE)
    uid = models.CharField(max_length=50)
    coordonnee = models.CharField(max_length=100)
    daty_time = models.DateTimeField()
    duration = models.IntegerField(null=True)
    id_trip = models.IntegerField(null=True)

class Statusparameter(models.Model):
    id = models.indexes
    status = models.CharField(max_length=50)
    min_percent = models.FloatField()
    max_percent = models.FloatField()
    couleur = models.CharField(max_length=50)
    desce = models.CharField(max_length=50, null=True)
    
class Statusparameterlib(models.Model):
    id = models.indexes
    status = models.CharField(max_length=50)
    min_percent = models.FloatField()
    max_percent = models.FloatField()
    couleur = models.CharField(max_length=50)
    desce = models.CharField(max_length=50, null=True)
    class Meta:
        managed = False
        db_table = 'suiviVehicule_statusparameterlib'
        
    def getListeParameters(self):
        return Statusparameterlib.objects.all().order_by('id')

class Recordcomment(models.Model):
    id = models.indexes
    id_trip = models.IntegerField(null=False)
    comment = models.TextField(max_length=500)
    datetime = models.DateTimeField()
    etat = models.IntegerField(default=0)

class Recordcommenttrajet(models.Model):
    id = models.indexes
    id_trip = models.IntegerField(null=False)
    comment = models.TextField(max_length=500)
    vehicleno = models.CharField(max_length=100)
    driver_oname = models.CharField(max_length=150)
    FromPlace = models.CharField(max_length=150)
    ToPlace = models.CharField(max_length=150)
    trip_start_time = models.TimeField()
    trip_start_date = models.CharField(max_length=15, null=False)
    pick_up_time = models.TimeField()
    status = models.CharField(max_length=100, null=True)
    couleur = models.CharField(max_length=100, null=True)
    daterecord = models.DateField()
    etat = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'suiviVehicule_recordtrajet'


