from datetime import date
import datetime

from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.

class Units(models.Model):
    Uid = models.CharField(max_length=50, null=True)
    Name = models.CharField(max_length=100, null=True)
    IMEI = models.CharField(max_length=100, null=True)
    Status = models.CharField(max_length=50, null=True)
    GroupName = models.CharField(max_length=100, null=True)
    CompanyName = models.CharField(max_length=100, null=True)
    PhoneNumber = models.CharField(max_length=100, null=True)
    UnitType = models.CharField(max_length=100, null=True)


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
    estimatetime = models.CharField(max_length=50, null=True)
    datetime = models.CharField(max_length=15, null=False)
    Uid = models.CharField(max_length=50, null=True)
    idstatusposdetail = models.IntegerField(null=True)
    trip_start_time = models.TimeField()
    idstatusparameter = models.IntegerField(null=True)
    difftimestart = models.FloatField()
    difftimepickup = models.FloatField()
    lateby = models.FloatField()
    current = models.CharField(max_length=150, null=True)
    annulated = models.FloatField(default=0)
    risky = models.FloatField(default=0)
    completed = models.FloatField(default=0)
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
    uid = models.CharField(max_length=50, null=True)
    coordonnee = models.CharField(max_length=100)
    daty_time = models.DateTimeField()
    duration = models.IntegerField(null=True)
    id_trip = models.IntegerField(null=True)
    current = models.CharField(max_length=150, null=True)
    distance = models.FloatField(null=True)
    daty_api_google = models.DateTimeField(null=True)
    is_call_api = models.IntegerField(null=True)
    speed = models.IntegerField(default=0)
    speedMeasure = models.CharField(max_length=150, default="kph")
    odometer = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    ignition = models.CharField(max_length=150, null=True)
    engineTime = models.CharField(max_length=150, null=True)
    engineStatus = models.CharField(max_length=150, null=True)
    modified = models.IntegerField(default=0)
    annulated = models.FloatField(default=0)
    risky = models.FloatField(default=0)
    completed = models.FloatField(default=0)

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
    vehicleno = models.CharField(max_length=100, null=True)
    driver_oname = models.CharField(max_length=150, null=True)
    FromPlace = models.CharField(max_length=150, null=True)
    ToPlace = models.CharField(max_length=150, null=True)
    trip_start_date = models.CharField(max_length=15, null=True)
    pick_up_time = models.TimeField(null=True)
    datetime = models.DateTimeField()
    etat = models.IntegerField(default=0)
    driver_mobile_number = models.CharField(max_length=50, null=True)
    current = models.CharField(max_length=150, null=True)
    difftimestart = models.FloatField(null=True)
    difftimepickup = models.FloatField(null=True)
    speed = models.DecimalField(default=0.0, max_digits=5, decimal_places=2)
    speedMeasure = models.CharField(max_length=150, default="kph")
    odometer = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    ignition = models.CharField(max_length=150, null=True)
    engineTime = models.DecimalField(default=0.0, max_digits=10, decimal_places=1)
    engineStatus = models.CharField(max_length=150, null=True)
    catno = models.IntegerField(default=0)
    


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
    current = models.CharField(max_length=150, null=True)
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


class Recordexport(models.Model):
    id = models.indexes
    id_trip = models.IntegerField(null=False)
    comment = models.TextField(max_length=500)
    vehicleno = models.CharField(max_length=100)
    driver_oname = models.CharField(max_length=150)
    FromPlace = models.CharField(max_length=150)
    ToPlace = models.CharField(max_length=150)
    trip_start_date = models.CharField(max_length=15, null=False)
    pick_up_time = models.CharField(max_length=50)
    status = models.CharField(max_length=100, null=True)
    couleur = models.CharField(max_length=100, null=True)
    daterecord = models.DateField()
    etat = models.IntegerField(default=0)
    driver_mobile_number = models.CharField(max_length=50)
    current = models.CharField(max_length=150, null=True)
    actualtime = models.CharField(max_length=50)
    difftimestart = models.FloatField(null=True)
    difftimepickup = models.FloatField(null=True)
    class Meta:
        managed = False
        db_table = 'suivivehicule_recordtrajet_export'


class Recaprefresh(models.Model):
    nbre_call_api = models.IntegerField()
    date = models.DateField()
    unitprice = models.DecimalField(default=0.0, max_digits=10, decimal_places=1)
    price = models.DecimalField(default=0.0, max_digits=10, decimal_places=1)
    class Meta:
        managed = False
        db_table = 'suivivehicule_recaprefresh_withprice'


class RefreshTime(models.Model):
    refresh_time = models.IntegerField()
    type = models.CharField(max_length=150)
    value = models.IntegerField(null=True)
    date_time = models.DateTimeField(auto_now_add=True)
    is_activate = models.BooleanField(default=True)
    desce = models.CharField(max_length=150, null=True)

    from django.db import models


class ReasonCancel(models.Model):
    reason_name = models.CharField(max_length=100)
    reason_description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)
    def __str__(self):
        return self.reason_name


class SubReasonCancel(models.Model):
    reason = models.ForeignKey(
        ReasonCancel, on_delete=models.CASCADE, related_name='sub_reasons')
    sub_reason_name = models.CharField(max_length=100)
    sub_reason_description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)
    def __str__(self):
        return self.sub_reason_name


class ReasonCancelRecord(models.Model):
    id = models.indexes
    reason = models.ForeignKey(
        ReasonCancel, on_delete=models.CASCADE, related_name='records')
    record_comment = models.ForeignKey(
        Recordcomment, on_delete=models.CASCADE, related_name='cancel_records')
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.BooleanField(default=True)

    def __str__(self):
        return f"Record for {self.reason} - {self.record_comment}"


class SubReasonCancelRecord(models.Model):
    id = models.indexes
    sub_reason = models.ForeignKey(
        SubReasonCancel, on_delete=models.CASCADE, related_name='sub_records')
    record_comment_sub = models.ForeignKey(
        Recordcomment, on_delete=models.CASCADE, related_name='sub_cancel_records')
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.BooleanField(default=True)

    def __str__(self):
        return f"Record for {self.sub_reason} - {self.record_comment_sub}"


class SubReasonCancelRecordV1(models.Model):
    id = models.IntegerField(primary_key=True)
    state = models.BooleanField()
    record_comment_sub_id = models.IntegerField()
    sub_reason_id = models.IntegerField()
    sub_reason_name = models.CharField(max_length=255)
    sub_reason_description = models.TextField()
    reason_name = models.CharField(max_length=255)
    reason_id = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'suivivehicule_subreasoncancelrecord_v1'

class StatusposMin(models.Model):
    uid = models.CharField(max_length=50, null=True)
    daty_time = models.DateTimeField()
    duration = models.IntegerField(null=True)
    id_trip = models.IntegerField(null=True)
    distance = models.FloatField(null=True)
    is_call_api = models.IntegerField(null=True)
    class Meta:
        managed = False
        db_table = 'suivivehicule_statuspos_min'
    
class BankPosition(models.Model):
    id_trip = models.IntegerField(null=True)
    uid = models.CharField(max_length=50, null=True)
    daty_time = models.DateTimeField()
    speed = models.DecimalField(default=0.0, max_digits=5, decimal_places=2)
    speedMeasure = models.CharField(max_length=150, default="kph")
    odometer = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    ignition = models.CharField(max_length=150, null=True)
    engineTime = models.DecimalField(default=0.0, max_digits=10, decimal_places=1)
    engineStatus = models.CharField(max_length=150, null=True)

class StatusPosMinBank(models.Model):
    id_trip = models.IntegerField(null=True)
    uid = models.CharField(max_length=50, null=True)
    daty_time = models.DateTimeField()
    duration = models.IntegerField(null=True)
    distance = models.FloatField(null=True)
    speed = models.DecimalField(default=0.0, max_digits=5, decimal_places=2)
    speedMeasure = models.CharField(max_length=150, default="kph")
    odometer = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    ignition = models.CharField(max_length=150, null=True)
    engineTime = models.DecimalField(default=0.0, max_digits=10, decimal_places=1)
    engineStatus = models.CharField(max_length=150, null=True)
    class Meta:
        managed = False
        db_table = 'suivivehicule_statuspos_min_transit'

class TrajetcoordonneeVehicleInfo(models.Model):
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
    datetime = models.CharField(max_length=15, null=False)
    Uid = models.CharField(max_length=50, null=True)
    idstatusposdetail = models.IntegerField(null=True)
    trip_start_time = models.TimeField()
    idstatusparameter = models.IntegerField(null=True)
    difftimestart = models.FloatField()
    difftimepickup = models.FloatField()
    lateby = models.FloatField()
    current = models.CharField(max_length=150, null=True)
    speed = models.DecimalField(default=0.0, max_digits=5, decimal_places=2)
    speedMeasure = models.CharField(max_length=150, default="kph")
    odometer = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    ignition = models.CharField(max_length=150, null=True)
    engineTime = models.DecimalField(default=0.0, max_digits=10, decimal_places=1)
    engineStatus = models.CharField(max_length=150, null=True)
    annulated = models.FloatField(default=0)
    risky = models.FloatField(default=0)
    completed = models.FloatField(default=0)

    class Meta:
        managed = False
        db_table = 'suivivehicule_laststatuswithvehiculeinfo'


class TripMessageSending(models.Model):
    name = models.CharField(max_length=150, null=True)
    id_trip = models.IntegerField(null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_send = models.BooleanField(default=False)

class TripMessageSendingLib(models.Model):
    name = models.CharField(max_length=150, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_send = models.BooleanField(default=False)
    vehicleno = models.CharField(max_length=100)
    driver_oname = models.CharField(max_length=150)
    driver_mobile_number = models.CharField(max_length=50)
    FromPlace = models.CharField(max_length=150)
    ToPlace = models.CharField(max_length=150)
    id_trip = models.IntegerField()
    pick_up_time = models.TimeField()
    PickUp_H_Pos = models.CharField(max_length=100)
    resa_trans_type = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'suivivehicule_tripmessagesendinglib'

class VehicleFleetStatistics(models.Model):
    available_vehicles = models.IntegerField()
    notavailable_vehicles = models.IntegerField()
    active_users = models.IntegerField()
    current_trips = models.IntegerField()
    last_google_api_call = models.IntegerField()
    trips_today = models.IntegerField()

    class Meta:
        managed = False  
        db_table = 'vehicle_fleet_statistics' 
        auto_created = True 

    def __str__(self):
        return f"Stats: {self.available_vehicles} vehicles, {self.active_users} users"
    
class PlanningWeekMoy(models.Model):
    year = models.IntegerField() 
    month = models.IntegerField() 
    week = models.IntegerField() 
    total_plannings = models.IntegerField() 
    average_plannings_per_day = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)

    class Meta:
        managed = False  
        db_table = 'planning_week_moy' 
        auto_created = True 

class PlanningDriverMonth(models.Model):
    driver_oname = models.CharField(max_length=100)
    driver_mobile_number = models.CharField(max_length=100)
    nombre_trajets = models.IntegerField()
    class Meta:
        managed = False  
        db_table = 'planning_driver_month' 
        auto_created = True 

class TrajetPerformanceSummary(models.Model):
    total_trips = models.IntegerField()
    completed_trips = models.IntegerField()
    completed_percentage = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    late_trips = models.IntegerField()
    late_percentage = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    canceled_trips = models.IntegerField()
    canceled_percentage = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    trip_day = models.DateField(primary_key=True)
    class Meta:
        managed = False  
        db_table = 'trajet_performance_summary' 
        auto_created = True 

class TrajetDetailInfoVehicule(models.Model):
    id_trip = models.IntegerField()
    duration = models.CharField(max_length=100, null=True)
    daty_time = models.CharField(max_length=15, null=False)
    Uid = models.CharField(max_length=50, null=True)
    current = models.CharField(max_length=150, null=True)
    speed = models.DecimalField(default=0.0, max_digits=5, decimal_places=2)
    speedMeasure = models.CharField(max_length=150, default="kph")
    odometer = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    ignition = models.CharField(max_length=150, null=True)
    engineTime = models.DecimalField(default=0.0, max_digits=10, decimal_places=1)
    engineStatus = models.CharField(max_length=150, null=True)
    annulated = models.FloatField(default=0)
    risky = models.FloatField(default=0)
    completed = models.FloatField(default=0)
    
    class Meta:
        managed = False
        db_table = 'suivivehicule_detailinfovehicule'

class TypeRapport(models.Model):
    type = models.CharField(max_length=100, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

class RapportAuto(models.Model):
    title = models.CharField(max_length=100, null=True)
    type_rapport = models.ForeignKey(TypeRapport, on_delete=models.CASCADE, related_name='type_rapport')
    sent_to = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="sent_to")
    description = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

class LogRapportAuto(models.Model):
    rapport_auto = models.ForeignKey(RapportAuto, on_delete=models.CASCADE, related_name="rapport_auto")
    recipient = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_to", null=True)
    result = models.TextField()
    status = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class RapportAutoView(models.Model):
    rapport_title = models.CharField(max_length=100, null=True)
    rapport_description = models.TextField()
    rapport_created_at = models.DateTimeField()
    rapport_is_active = models.BooleanField()
    type_rapport_id = models.IntegerField()
    type_rapport_type = models.CharField(max_length=100, null=True)
    type_rapport_description = models.TextField()
    type_rapport_created_at = models.DateTimeField()
    type_rapport_is_active = models.BooleanField()
    group_id = models.IntegerField()
    group_name = models.CharField(max_length=150)

    class Meta:
        managed = False  
        db_table = 'rapport_auto_view'

class LogRapportAutoView(models.Model):
    log_recipient = models.CharField(max_length=100, null=True)
    log_result = models.TextField()
    log_status = models.CharField(max_length=100, null=True)
    log_created_at = models.DateTimeField()
    rapport_id = models.IntegerField()
    rapport_title = models.CharField(max_length=100, null=True)
    rapport_description = models.TextField()
    rapport_created_at = models.DateTimeField()
    rapport_is_active = models.BooleanField()
    type_rapport_id = models.IntegerField()
    type_rapport_type = models.CharField(max_length=100, null=True)
    type_rapport_description = models.TextField()
    type_rapport_is_active = models.BooleanField()
    user_id = models.IntegerField(null=True)
    user_username = models.CharField(max_length=150, null=True)
    user_email = models.EmailField(null=True)

    class Meta:
        managed = False 
        db_table = 'log_rapport_auto_view'  
    

    

    