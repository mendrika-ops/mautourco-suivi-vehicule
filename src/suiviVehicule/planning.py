from datetime import datetime
from suiviVehicule.models import Planning, Planninglib, Trajetcoordonnee


class planning():
    def verify_planning(self, planning, now):
        str(now.strftime('%Y-%m-%d'))
        datenow = datetime. strptime(str(now.strftime('%Y-%m-%d')), '%Y-%m-%d')
        bool = Planninglib.objects.filter(daterecord=datenow, id_trip=planning.id_trip, vehicleno__icontains=planning.vehicleno).exists()
        if bool is False:
            planning.save()

    def save_planning(self, data, now):
        planning = Planning()
        
        setattr(planning, 'vehicleno', data[0].strip())
        setattr(planning, 'driver_oname', data[1].strip())
        setattr(planning, 'driver_mobile_number', '-' if data[2] is None else data[2].strip())
        setattr(planning, 'FromPlace', data[3])
        setattr(planning, 'ToPlace', data[4])
        setattr(planning, 'id_trip', data[5])
        setattr(planning, 'trip_no', data[6])
        setattr(planning, 'trip_start_date', data[7])
        setattr(planning, 'pick_up_time', data[8])
        setattr(planning, 'PickUp_H_Pos', data[9])
        setattr(planning, 'resa_trans_type', data[10])
        setattr(planning, 'daty_time', now)
        setattr(planning, 'gpsid', data[11])

        self.verify_planning(planning, now)
        
    def save_trajetcoordonne(self, data, refresh_id):
        trajetcoordonnee = Trajetcoordonnee()
        
        setattr(trajetcoordonnee, 'vehicleno', data[0].strip())
        setattr(trajetcoordonnee, 'driver_oname', '-' if data[1] is None else data[1].strip())
        setattr(trajetcoordonnee, 'driver_mobile_number', '-' if data[2] is None else data[2].strip())
        setattr(trajetcoordonnee, 'FromPlace', data[3])
        setattr(trajetcoordonnee, 'ToPlace', data[4])
        setattr(trajetcoordonnee, 'id_trip', data[5])
        setattr(trajetcoordonnee, 'trip_no', data[6])
        setattr(trajetcoordonnee, 'trip_start_date', data[7])
        setattr(trajetcoordonnee, 'pick_up_time', data[8])
        setattr(trajetcoordonnee, 'PickUp_H_Pos', data[9])
        setattr(trajetcoordonnee, 'refresh_id', refresh_id)

        trajetcoordonnee.save()


    def get_list_planning(self, datefrom, dateto):
        dateinfrom = datetime. strptime(datefrom, '%Y-%m-%d')
        dateinto = datetime. strptime(dateto, '%Y-%m-%d')
        return Planninglib.objects.filter(daterecord__range = [dateinfrom,dateinto]).order_by('-daterecord','-actualtime')
        

        
