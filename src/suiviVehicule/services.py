import pytz
import requests
from django.db import IntegrityError, connection, connections, transaction
from humanfriendly import format_timespan
from django.conf import settings
from suiviVehicule.models import Recordcomment, Statusparameter, Statusparameterlib,Statuspos, TrajetcoordonneeWithUid, UidName, Statusposdetail, Trajetcoordonnee, TrajetcoordonneeSamm, Recordcommenttrajet
from datetime import datetime


class services():
    UserIdGuid = settings.USERIDGUID
    SessionId = settings.SESSIONID

    def get_api_data(self):
        response = requests.get(
            f'https://api.3dtracking.net/api/v1.0/Units/Unit/List?UserIdGuid={self.UserIdGuid}&SessionId={self.SessionId}')
        users = response.json()
        if response.status_code == 400:
            raise Exception("Error 400 ! Please check your connection")
        return users

    def get_position_at_time(self, uid, date_time):
        req = f"https://api.3dtracking.net/api/v1.0/Units/{uid}/PositionAtTime?UserIdGuid={self.UserIdGuid}&SessionId={self.SessionId}&PointInTimeDateTimeUTC={date_time}"
        response = requests.get(req)
        pos = response.json()
        if response.status_code == 400:
            raise Exception("Error 400 ! Please check your connection")
        return pos

    def get_position_lat_long(self, uid, date_time):
        pos = self.get_position_at_time(uid, date_time)
        lat = pos["Result"]["Position"]["Latitude"]
        long = pos["Result"]["Position"]["Longitude"]
        status_detail = Statusposdetail()
        setattr(status_detail, 'uid', uid)
        setattr(status_detail, 'coordonnee', f"{lat},{long}")
        return status_detail

    def get_direction(self, origin, destination):
        waypoints = f'{origin}|{destination}'
        currentposition = ""
        result = requests.get(
            'https://maps.googleapis.com/maps/api/directions/json?',
            params={
                'origin': origin,
                'destination': destination,
                'waypoints': waypoints,
                "key": 'AIzaSyCJwwTnRM8ePI1yj_zyOGgBtepyyJur8Gs'
            })

        directions = result.json()
        #print("Direction ::: ",directions)
        if directions["status"] == "OK":

            routes = directions["routes"][0]["legs"]

            distance = 0
            duration = 0
            route_list = []

            for route in range(len(routes)):
                distance += int(routes[route]["distance"]["value"])
                duration += int(routes[route]["duration"]["value"])
                
                route_step = {
                    'origin': routes[route]["start_address"],
                    'destination': routes[route]["end_address"],
                   
                }
                route_list.append(route_step)
            current = route_list[len(routes)-1]["destination"].split(", ")
            currentposition = current[0] + ", "+ current[1]
        print(currentposition)
        return {
            "origin": origin,
            "destination": destination,
            "distance": round(distance, 2),
            "duration": duration, 
            "current": currentposition
        }

    def set_one_refresh(self, idstatusdetail, id):
        try:
            data = Statusposdetail.objects.get(pk=idstatusdetail)
            trajet = TrajetcoordonneeSamm.objects.get(pk=id)
            currentdate = datetime.now()
            date_time = currentdate.strftime("%d %B %Y %H:%M:%S")
            status_detail = self.get_position_lat_long(data.uid, date_time)
            file = self.get_direction(trajet.PickUp_H_Pos, status_detail.coordonnee)
            setattr(data, 'id', idstatusdetail)
            setattr(data, 'daty_time', currentdate)
            setattr(data, 'duration', file["duration"])
            data.save()
            #self.create_comment(data.id_trip,trajet.idstatusparameter, currentdate)
        except Exception as e:
            raise e
    def add_log(self, now):
        list_uid = TrajetcoordonneeSamm.objects.all().order_by('idstatusparameter','-trip_start_date', 'pick_up_time')
        for row in list_uid:
            self.create_comment(row, now)

    #@transaction.atomic            
    def gestion_status_pos(self):
        status = Statuspos()
        try:
            #list_uid = TrajetcoordonneeSamm.objects.all().order_by('idstatusparameter','-trip_start_date', 'pick_up_time')
            #if len(list_uid) < 1:
            #    list_uid = self.get_new_data()
            list_uid = self.get_new_data()
            currentdate = datetime.now()
            now = currentdate
            date_time = now.strftime("%d %B %Y %H:%M:%S")
            setattr(status, 'datetime', now)
            setattr(status, 'desc', 'opp')
            status.save()
            #sid = transaction.savepoint()
            for row in list_uid:
                status_detail = self.get_position_lat_long(row.Uid, date_time)
                file = self.get_direction(row.PickUp_H_Pos, status_detail.coordonnee)
                print("UID ", row.Uid, "coordonnee 000 ", row.PickUp_H_Pos, " COORDONNEE 111 ",
                    status_detail.coordonnee," distance ",file["distance"])
                setattr(status_detail, 'idmere', status)
                setattr(status_detail, 'duration', file["duration"])
                setattr(status_detail, 'daty_time', now)
                setattr(status_detail, 'id_trip', row.id_trip)
                setattr(status_detail, 'current', file["current"])
                setattr(status_detail, 'distance', file["distance"])
                status_detail.save()
            self.add_log(now)
            #transaction.savepoint_commit(sid)
        except IntegrityError:
            print("error")
            #transaction.savepoint_rollback(sid)
        return status

    def get_last_refresh(self):
        data = []
        obj = None
        cursor = connection.cursor()
        cursor.execute(
            "select max(datetime) From suiviVehicule_statuspos")
        for row in cursor:
            data.append(row[0])
        if len(data) < 1:
            obj = None
        else:
            obj = data[0]
        return obj

    def get_data(self, form, page,defaut):
        data = []
        if form.is_valid():
            data = TrajetcoordonneeSamm.objects.filter(driver_oname__icontains=form.cleaned_data['driver_oname'],
                                                   driver_mobile_number__icontains=form.cleaned_data[
                                                       'driver_mobile_number'],
                                                   vehicleno__icontains=form.cleaned_data['vehicleno'],
                                                   FromPlace__icontains=form.cleaned_data['FromPlace'],
                                                   ToPlace__icontains=form.cleaned_data['ToPlace'],
                                                   status__icontains=form.cleaned_data['status']).order_by('idstatusparameter',
            '-trip_start_date', 'pick_up_time')[0:page+defaut]
        else :
            data = TrajetcoordonneeSamm.objects.all().order_by('idstatusparameter','-trip_start_date', 'pick_up_time')[0:page+defaut]
        trajetcoord = []
        for trajet in data:
            setattr(trajet, 'duration', str(trajet.duration))
            trajetcoord.append(trajet)
        return trajetcoord
    
    def get_new_data(self):
        return TrajetcoordonneeWithUid.objects.all().order_by('-trip_start_date', 'pick_up_time')
      
    def data_chart(self):
        label = []
        data = []
        couleur = []
        cursor = connection.cursor()
        req = "select sl.status , count(sl.status), sl.couleur from suivivehicle_laststatus sl group by sl.status,sl.couleur"
        cursor.execute(req)
        for row in cursor:
            label.append(row[0])
            data.append(row[1])
            couleur.append(row[2])
        return {
            "label": label,
            "data": data,
            "couleur": couleur
        }
    
    def check_comment(self, id_trip):
        return Recordcomment.objects.filter(id_trip=id_trip)
    
    def boolean_parameter_for_log(self, idstatus):
        return Statusparameter.objects.filter(id=idstatus).exclude(status__icontains="On Track").exists()
    
    def getall_data_count(self,form):
        data = []
        if form.is_valid():
             data = TrajetcoordonneeSamm.objects.filter(driver_oname__icontains=form.cleaned_data['driver_oname'],
                                                   driver_mobile_number__icontains=form.cleaned_data[
                                                       'driver_mobile_number'],
                                                   vehicleno__icontains=form.cleaned_data['vehicleno'],
                                                   FromPlace__icontains=form.cleaned_data['FromPlace'],
                                                   ToPlace__icontains=form.cleaned_data['ToPlace'],
                                                   status__icontains=form.cleaned_data['status']).count()
        else:
            data = TrajetcoordonneeSamm.objects.all().count()
        return data
    
    def create_comment(self, row, now):
        try:
            if self.boolean_parameter_for_log(row.idstatusparameter) is True:
                check = self.check_comment(row.id_trip) 
                if len(check) > 0:
                    if check[0].etat != 0: 
                        check[0].etat = row.idstatusparameter
                        check[0].datetime = now
                        check[0].save()
                else:
                    record = Recordcomment()
                    record.comment = ""
                    record.id_trip = row.id_trip
                    record.vehicleno = row.vehicleno
                    record.driver_oname = row.driver_oname
                    record.FromPlace = row.FromPlace
                    record.ToPlace = row.ToPlace
                    record.trip_start_date = row.trip_start_date
                    record.pick_up_time = row.pick_up_time
                    record.driver_mobile_number = row.driver_mobile_number
                    record.datetime = now 
                    record.etat = row.idstatusparameter
                    record.save()
        except Exception as e:
            raise e

    def data_chart_calcule(self, data):
        try:
            late = 0
            ontime = 0
            risky = 0
            terminated = 0
            label= []
            couleur = []
            stat = Statusparameter.objects.filter(desce=1).order_by('id')
            if len(stat) < 1:
                raise Exception("Status data not found")
            for trajet in stat:
                label.append(trajet.status)
                couleur.append(trajet.couleur)

            # label = ['Risky', 'On time', 'Terminated', 'Late']
            # couleur = ['rgba(255,192,59,1.0)', 'rgba(30,132,127,1.0)', 'rgba(196,196,196,1.0)','rgba(255,110,64,1.0)']
            for row in data:
                if row.status == 'On time':
                    ontime += 1
                elif row.status == 'Late':
                    late += 1
                elif row.status == 'Risky':
                    risky += 1
                elif row.status == 'Terminated':
                    terminated += 1
        except Exception as e:
            raise e
        return {
            "label": label,
            "data": [risky, late],
            "couleur": couleur
        }
    
    def get_listes_record(self,datefrom,dateto):
        dateinfrom = datetime. strptime(datefrom, '%Y-%m-%d')
        dateinto = datetime. strptime(dateto, '%Y-%m-%d')
        liste = Recordcommenttrajet.objects.filter(daterecord__range = [dateinfrom,dateinto]).order_by('-daterecord')
        return liste
    
    def get_liste_parameter(self):
        return Statusparameterlib().getListeParameters()
    
    def get_liste_parameter_activate(self):
        return Statusparameter.objects.filter(desce=1).order_by('min_percent')
    def get_liste_parameter_byId(self, id):
        tab = []
        try:
            if(id is None):
                raise Exception("Id not found")
            tab = Statusparameter.objects.get(id=id)
        except Exception as e:
            raise e
        return tab
    
    def get_asterix_data(self):
        tab = []
        cursor = connections["asterix"].cursor()
        req = "SELECT v.vehicleno,CONCAT(d.driver_sname,' ',d.`driver_oname`) AS driver_oname,d.MobileNo AS driver_mobile_number,h.h_name AS FromPlace,h1.`h_name` AS ToPlace,t.id_trip,t.`trip_no`,t.`trip_start_date`,t.`pick_up_time` AS pick_up_time,CONCAT(h.`latitude`, ',', h.`longitude`) AS PickUp_H_Pos,t.resa_trans_type FROM trip t,driver d,hotel h,hotel h1,vehicle v WHERE trip_start_date = CURRENT_DATE() AND t.`id_driver` = d.`id_driver` AND v.id_vehicle = t.id_vehicle AND t.`pick_up_place_id` = h.`id_hotel` AND t.`destination_id` = h1.`id_hotel` AND t.resa_type IN (1, 2, 3, 4, 5) AND v.vehicleno != 'CANCELLED' AND t.vehicleno != 'Not Assigned' AND t.resa_trans_type != '' AND t.`pick_up_time` BETWEEN CURRENT_TIME AND ADDTIME(CURRENT_TIME,30000) GROUP BY trip_no, FromPlace ORDER BY t.trip_start_date, t.`pick_up_time`, t.`trip_no`"
       
        cursor.execute(req)
        for row in cursor:
            trajetcoordonnee = Trajetcoordonnee()
            trajetcoordonnee.set_vehicleno(row[0])
            trajetcoordonnee.set_driver_oname(row[1])
            trajetcoordonnee.set_driver_mobile_number(row[2])
            trajetcoordonnee.set_FromPlace(row[3])
            trajetcoordonnee.set_ToPlace(row[4])
            trajetcoordonnee.set_id_trip(row[5])
            trajetcoordonnee.set_trip_no(row[6])
            trajetcoordonnee.set_trip_start_date(row[7])
            trajetcoordonnee.set_pick_up_time(row[8])
            trajetcoordonnee.set_PickUp_H_Pos(row[9])
            tab.append(trajetcoordonnee)
            print(trajetcoordonnee.get_id_trip())
        return tab
    
    def rechange(self):
        tab = self.get_asterix_data()
        Trajetcoordonnee.objects.all().delete()
        for row in tab:
            row.save()
        