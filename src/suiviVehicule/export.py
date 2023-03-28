
from django.db import models

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
    current = models.CharField(max_length=150,null=True)
    actualtime = models.CharField(max_length=50)
    difftimestart = models.FloatField(null=True)
    difftimepickup = models.FloatField(null=True)
    class Meta:
        managed = False
        db_table = 'suivivehicule_recordtrajet_export'