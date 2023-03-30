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
class Units(models.Model):
    Uid = models.CharField(max_length=50, null=True)
    Name = models.CharField(max_length=100, null=True)
    IMEI = models.CharField(max_length=100, null=True)
    Status = models.CharField(max_length=50, null=True)
    GroupName = models.CharField(max_length=100, null=True)
    CompanyName = models.CharField(max_length=100, null=True)
    PhoneNumber = models.CharField(max_length=100, null=True)
    UnitType = models.CharField(max_length=100, null=True)

    def set_Uid(self, Uid):
        self.Uid = Uid
    def set_Name(self, Name):
        self.Name = Name
    def set_IMEI(self, IMEI):
        self.IMEI = IMEI
    def set_Status(self, Status):
        self.Status = Status
    def set_GroupName(self, GroupName):
        self.GroupName = GroupName
    def set_CompanyName(self, CompanyName):
        self.CompanyName = CompanyName
    def set_PhoneNumber(self, PhoneNumber):
        self.PhoneNumber = PhoneNumber
    def set_UnitType(self, UnitType):
        self.UnitType = UnitType

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
    difftimestart = models.FloatField()
    difftimepickup = models.FloatField()
    current = models.CharField(max_length=150,null=True)
    class Meta:
        managed = False
        db_table = 'suivivehicle_laststatus'

class Refresh(models.Model):
    id = models.indexes
    date_time = models.DateTimeField()

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
    trip_start_time = models.TimeField(null=True)
    refresh = models.ForeignKey(Refresh, on_delete=models.CASCADE, null=True)
        
    def get_vehicleno(self):
        return self.vehicleno
    def set_vehicleno(self, vehiculeno):
        self.vehicleno = vehiculeno
    
    def get_driver_oname(self):
        return self.driver_oname
    def set_driver_oname(self, driver_oname):
        self.driver_oname = driver_oname
    
    def get_driver_mobile_number(self):
        return self.driver_mobile_number
    def set_driver_mobile_number(self, driver_mobile_number):
        self.driver_mobile_number= driver_mobile_number

    def get_FromPlace(self):
        return self.FromPlace
    def set_FromPlace(self, FromPlace):
        self.FromPlace = FromPlace

    def get_ToPlace(self):
        return self.ToPlace
    def set_ToPlace(self, ToPlace):
        self.ToPlace = ToPlace

    def get_id_trip(self):
        return self.id_trip
    def set_id_trip(self, id_trip):
        self.id_trip = id_trip

    def get_trip_no(self):
        return self.trip_no
    def set_trip_no(self, trip_no):
        self.trip_no = trip_no

    def get_trip_start_date(self):
        return self.trip_start_date
    def set_trip_start_date(self, trip_start_date):
        self.trip_start_date = trip_start_date

    def get_pick_up_time(self):
        return self.pick_up_time
    def set_pick_up_time(self, pick_up_time):
        self.pick_up_time = pick_up_time
    
    def get_PickUp_H_Pos(self):
        return self.PickUp_H_Pos
    def set_PickUp_H_Pos(self, PickUp_H_Pos):
        self.PickUp_H_Pos = PickUp_H_Pos

    
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
    nbre = models.IntegerField(null=True)


class Statusposdetail(models.Model):
    id = models.indexes
    idmere = models.ForeignKey(Statuspos, on_delete=models.CASCADE)
    uid = models.CharField(max_length=50,null=True)
    coordonnee = models.CharField(max_length=100)
    daty_time = models.DateTimeField()
    duration = models.IntegerField(null=True)
    id_trip = models.IntegerField(null=True)
    current = models.CharField(max_length=150,null=True)
    distance = models.FloatField(null=True)



class Statusparameter(models.Model):
    id = models.indexes
    status = models.CharField(max_length=50)
    min_percent = models.FloatField()
    max_percent = models.FloatField()
    couleur = models.CharField(max_length=50)
    desce = models.CharField(max_length=50, null=True)
    max_distance = models.FloatField(null=True)
    
class Statusparameterlib(models.Model):
    id = models.indexes
    status = models.CharField(max_length=50)
    min_percent = models.FloatField()
    max_percent = models.FloatField()
    couleur = models.CharField(max_length=50)
    desce = models.CharField(max_length=50, null=True)
    max_distance = models.FloatField(null=True)
    class Meta:
        managed = False
        db_table = 'suiviVehicule_statusparameterlib'
        
    def getListeParameters(self):
        return Statusparameterlib.objects.all().order_by('min_percent')

class Recordcomment(models.Model):
    id = models.indexes
    id_trip = models.IntegerField(null=False)
    comment = models.TextField(max_length=500)
    vehicleno = models.CharField(max_length=100,null=True)
    driver_oname = models.CharField(max_length=150,null=True)
    FromPlace = models.CharField(max_length=150,null=True)
    ToPlace = models.CharField(max_length=150,null=True)
    trip_start_date = models.CharField(max_length=15, null=True)
    pick_up_time = models.TimeField(null=True)
    datetime = models.DateTimeField()
    etat = models.IntegerField(default=0)
    driver_mobile_number = models.CharField(max_length=50,null=True)
    current = models.CharField(max_length=150,null=True)
    difftimestart = models.FloatField(null=True)
    difftimepickup = models.FloatField(null=True)
class Recordcommenttrajet(models.Model):
    id = models.indexes
    id_trip = models.IntegerField(null=False)
    comment = models.TextField(max_length=500)
    vehicleno = models.CharField(max_length=100)
    driver_oname = models.CharField(max_length=150)
    FromPlace = models.CharField(max_length=150)
    ToPlace = models.CharField(max_length=150)
    trip_start_date = models.CharField(max_length=15, null=False)
    pick_up_time = models.TimeField()
    status = models.CharField(max_length=100, null=True)
    couleur = models.CharField(max_length=100, null=True)
    daterecord = models.DateField()
    etat = models.IntegerField(default=0)
    driver_mobile_number = models.CharField(max_length=50)
    current = models.CharField(max_length=150,null=True)
    actualtime = models.TimeField()
    difftimestart = models.FloatField(null=True)
    difftimepickup = models.FloatField(null=True)
    class Meta:
        managed = False
        db_table = 'suiviVehicule_recordtrajet'

class Planning(models.Model):
    Planning_id = models.indexes
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
    resa_trans_type = models.CharField(max_length=100)
    daty_time = models.DateTimeField(null=True)
    gpsid = models.CharField(null=True, max_length=100)
    
    def set_vehicleno(self, vehiculeno):
        self.vehicleno = vehiculeno

    def set_driver_oname(self, driver_oname):
        self.driver_oname = driver_oname
   
    def set_driver_mobile_number(self, driver_mobile_number):
        self.driver_mobile_number= driver_mobile_number

    def set_FromPlace(self, FromPlace):
        self.FromPlace = FromPlace

    def set_ToPlace(self, ToPlace):
        self.ToPlace = ToPlace

    def set_id_trip(self, id_trip):
        self.id_trip = id_trip

    def set_trip_no(self, trip_no):
        self.trip_no = trip_no

    def set_trip_start_date(self, trip_start_date):
        self.trip_start_date = trip_start_date

    def set_pick_up_time(self, pick_up_time):
        self.pick_up_time = pick_up_time
    
    def set_PickUp_H_Pos(self, PickUp_H_Pos):
        self.PickUp_H_Pos = PickUp_H_Pos

    def set_resa_trans_type(self, resa_trans_type):
        self.resa_trans_type = resa_trans_type

class Planninglib(models.Model):
    id = models.indexes
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
    resa_trans_type = models.CharField(max_length=100)
    daty_time = models.DateTimeField(null=True)
    daterecord = models.DateField(null=True)
    actualtime = models.TimeField(null=True)
    gpsid = models.CharField(null=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'suivivehicule_planninglib'

class Recaprefresh(models.Model):
    nbre_refresh = models.IntegerField()
    nbre_call_api = models.IntegerField()
    date = models.DateField()
    class Meta:
        managed = False
        db_table = 'suivivehicule_recaprefresh'


