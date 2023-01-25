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


class UidName(models.Model):
    vehicleno = models.CharField(max_length=100)
    Uid = models.CharField(max_length=50)

    def __init__(self, vehicleno, Uid):
        self.vehicleno = vehicleno
        self.Uid = Uid

class Statuspos(models.Model):
    id = models.indexes
    datetime = models.DateTimeField()
    desc = models.CharField(max_length=100)


class Statusposdetail(models.Model):
    id = models.indexes
    idmere = models.ForeignKey(Statuspos, on_delete=models.CASCADE)
    uid = models.CharField(max_length=50)
    coordonnee = models.CharField(max_length=100)

