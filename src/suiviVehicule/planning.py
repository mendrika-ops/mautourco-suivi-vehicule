from datetime import datetime
from suiviVehicule.models import Planning, Planninglib, Trajetcoordonnee


class planning():
    def verify_planning(self, planning, now):
        str(now.strftime('%Y-%m-%d'))
        datenow = datetime. strptime(str(now.strftime('%Y-%m-%d')), '%Y-%m-%d')
        bool = Planning.objects.filter(trip_start_date=datenow, id_trip=planning.id_trip, vehicleno__icontains=planning.vehicleno).exists()
        if bool is False:
            planning.save()

    def save_planning(self, data, now):
        planning = Planning()
        planning.set_vehicleno(data[0])
        planning.set_driver_oname(data[1])
        planning.set_driver_mobile_number(data[2])
        planning.set_FromPlace(data[3])
        planning.set_ToPlace(data[4])
        planning.set_id_trip(data[5])
        planning.set_trip_no(data[6])
        planning.set_trip_start_date(data[7])
        planning.set_pick_up_time(data[8])
        planning.set_PickUp_H_Pos(data[9])
        planning.set_resa_trans_type(data[10])
        planning.daty_time = now
        self.verify_planning(planning,now)

    def save_trajetcoordonne(self, data, refresh_id):
        trajetcoordonnee = Trajetcoordonnee()
        trajetcoordonnee.set_vehicleno(data[0])
        trajetcoordonnee.set_driver_oname(data[1])
        trajetcoordonnee.set_driver_mobile_number(data[2])
        trajetcoordonnee.set_FromPlace(data[3])
        trajetcoordonnee.set_ToPlace(data[4])
        trajetcoordonnee.set_id_trip(data[5])
        trajetcoordonnee.set_trip_no(data[6])
        trajetcoordonnee.set_trip_start_date(data[7])
        trajetcoordonnee.set_pick_up_time(data[8])
        trajetcoordonnee.set_PickUp_H_Pos(data[9])
        trajetcoordonnee.refresh_id = refresh_id

        trajetcoordonnee.save()

    def get_list_planning(self, datefrom, dateto):
        dateinfrom = datetime. strptime(datefrom, '%Y-%m-%d')
        dateinto = datetime. strptime(dateto, '%Y-%m-%d')
        return Planninglib.objects.filter(daterecord__range = [dateinfrom,dateinto]).order_by('-daterecord','-actualtime')
        

        
