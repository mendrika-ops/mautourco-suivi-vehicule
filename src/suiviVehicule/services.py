import pytz
import requests
from django.db import IntegrityError, connection, connections, transaction
from humanfriendly import format_timespan
from django.conf import settings
from suiviVehicule.models import Planning, Recaprefresh, Recordcomment, Refresh, Statusparameter, Statusparameterlib,Statuspos, TrajetcoordonneeWithUid, UidName, Statusposdetail, Trajetcoordonnee, TrajetcoordonneeSamm, Recordcommenttrajet, Units
from datetime import datetime,tzinfo
from dateutil import tz
import time
from suiviVehicule.planning import planning



class services():
    UserIdGuid=''
    SessionId=''
    UserName = 'devvirmatics@mautourco.com'
    Password = 'Mautourco@1234'
    minvalue = 2
    maxvalue = 15
    count_sleep = 0
    def get_api_data(self):
        response = requests.get(
            f'https://api.3dtracking.net/api/v1.0/Authentication/UserAuthenticate?UserName={self.UserName}&Password={self.Password}')
        users = response.json()
        self.UserIdGuid = users["Result"]["UserIdGuid"]
        self.SessionId = users["Result"]["SessionId"]
        if response.status_code == 400:
            raise Exception("Error 400 ! Please check your connection")
        

    def get_position_at_time(self, uid, date_time):
        # self.get_api_data()
        req = f"https://api.3dtracking.net/api/v1.0/Units/{uid}/PositionAtTime?UserIdGuid={self.UserIdGuid}&SessionId={self.SessionId}&PointInTimeDateTimeUTC={date_time}"
        response = requests.get(req)
        pos = response.json()
        if response.status_code == 400:
            raise Exception("Error 400 ! Please check your connection")
        #print("get api : ", pos)
        return pos
    
    def get_api_units(self):
        # self.get_api_data()
        req = f"https://api.3dtracking.net/api/v1.0/Units/Unit/List?UserIdGuid={self.UserIdGuid}&SessionId={self.SessionId}"
        response = requests.get(req)
        pos = response.json()
        if response.status_code == 400:
            raise Exception("Error 400 ! Please check your connection")
        #print("get api : ", pos)
        return pos

   

    def api_units(self):
        Units.objects.all().delete()
        units = self.get_api_units()
        result = units["Result"]
        for i in range(len(result)):
            #print(result[i]["Name"])
            units = Units()
            if self.is_exist_units(result[i]["Uid"].strip()) == False:
                units.set_Uid(result[i]["Uid"].strip())
                units.set_Name(result[i]["Name"].strip())
                units.set_IMEI(result[i]["IMEI"].strip())
                units.set_Status(result[i]["Status"])
                units.set_GroupName(result[i]["GroupName"])
                units.set_CompanyName(result[i]["CompanyName"])
                units.set_PhoneNumber(result[i]["PhoneNumber"])
                units.save()

    def is_exist_units(self, uid):
        return Units.objects.filter(Uid__icontains=uid).exists()

    def get_direction(self, origin, destination):
        waypoints = f'{origin}|{destination}'
        currentposition = ""
        try:
            result = requests.get(
                'https://maps.googleapis.com/maps/api/directions/json?',
                params={
                    'origin': origin,
                    'destination': destination,
                    'waypoints': waypoints,
                    'mode':'driving',
                    'key': 'AIzaSyA6wqUNamrQQTeq4zoW2zzHnNT4i35Tu-8'
                })

            directions = result.json()
            print("API Status ::: ", directions["status"])
            if directions["status"] == "OK":

                routes = directions["routes"][0]["legs"]

                distance = 0
                duration = 0
                route_list = []

                for route in range(len(routes)):
                    # print("routee " ,routes[route]["distance"])
                    # print("duration " ,routes[route]["duration"])
                    distance += round(int(routes[route]["distance"]["value"]))
                    duration += round(int(routes[route]["duration"]["value"]))
                    # print("approx im distance : ",round(int(routes[route]["distance"]["value"])))
                    # print("approx im duration : ",round(int(routes[route]["duration"]["value"])))
                    route_step = {
                        'origin': routes[route]["start_address"],
                        'destination': routes[route]["end_address"],
                    
                    }
                    route_list.append(route_step)
                current = route_list[len(routes)-1]["destination"].split(", ")
                currentposition = current[0] + ", "+ current[1]
                #print("total distance : ",distance)
                #print("total im duration : ",duration)
                return {
                    "origin": origin,
                    "destination": destination,
                    "distance": distance,
                    "duration": round(duration)+(60), 
                    "current": currentposition
                }
            
            elif directions["status"] == "INVALID_REQUEST":
                return None
            
            else:
                raise Exception("An ERROR API maps.googleapi.com")

        except Exception as e:
            print(e)
            raise e

    def set_one_refresh(self, idstatusdetail, id):
        try:
            data = Statusposdetail.objects.get(pk=idstatusdetail)
            trajet = TrajetcoordonneeSamm.objects.get(pk=id)
            currentdate = self.date_time()
            date_time = currentdate.strftime("%d %B %Y %H:%M:%S")
            status_detail = self.get_position_lat_long(data.uid, date_time)
            file = self.get_direction(status_detail.coordonnee, trajet.PickUp_H_Pos)
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

    def date_time(self):
        to_zone = tz.gettz('Indian/Mauritius')
        from_zone = tz.gettz('Indian/Mauritius')
        utc = datetime.now().replace(tzinfo=from_zone)
        central = utc.astimezone(to_zone)
        av = datetime.strptime(central.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        #print("date time :  ", av)
        #print("date now : ", datetime.now())
        return av
    
    def configuration_api_google(self, status_detail, row, pick_up, now, lat, long):
        file = []
        trip = Recordcommenttrajet.objects.filter(id_trip=row.id_trip,etat=1)
        last = Statusposdetail.objects.filter(id_trip=row.id_trip).order_by('-daty_time')
        if last.exists() is True and last[0].daty_api_google is not None:
            ref = now - last[0].daty_api_google.replace(tzinfo=None)
            ref_sec = ref.total_seconds()
            if trip.exists() is True:
            #if trip.exists() is True and ref_sec >= self.minvalue*60:
                self.count_sleep+=1
                if self.count_sleep >= 10:
                    print("sleep for 5 seconds")
                    time.sleep(5)
                    self.count_sleep = 0

                file = self.get_direction(f"{lat},{long}", pick_up[0]+","+pick_up[1])
                setattr(status_detail, 'daty_api_google', now)
                setattr(status_detail, 'is_call_api', 1)
                print("Appel:: offtrack :: reference ",round(ref_sec/60))
                
            elif trip.exists() is False:
            #elif trip.exists() is False and ref_sec >= self.maxvalue*60:
                self.count_sleep+=1
                if self.count_sleep >= 10:
                    print("sleep for 5 seconds")
                    time.sleep(5)
                    self.count_sleep = 0

                file = self.get_direction(f"{lat},{long}", pick_up[0]+","+pick_up[1])
                setattr(status_detail, 'daty_api_google', now)
                setattr(status_detail, 'is_call_api', 1)
                
                print("Appel:: ontrack :: reference ",round(ref_sec/60))
            else:
                file = {
                        "distance": last[0].distance,
                        "duration": last[0].duration
                    }
                setattr(status_detail, 'daty_api_google', last[0].daty_api_google)
                setattr(status_detail, 'is_call_api', 0)
                print("Appel:: ready :: reference ",round(ref_sec/60))
        else:
            print("Appel:: not in :: reference ")
            file = self.get_direction(f"{lat},{long}", pick_up[0]+","+pick_up[1])
            setattr(status_detail, 'daty_api_google', now)
            setattr(status_detail, 'is_call_api', 0)
        return file


    def get_position_lat_long(self, uid, date_time, row, status, now):
        status_detail = Statusposdetail()
        file = []
        try:
            if uid is not None:
                pos = self.get_position_at_time(uid, date_time)

                if pos["Status"]["Result"] != 'Error':
                    lat = pos["Result"]["Position"]["Latitude"]
                    long = pos["Result"]["Position"]["Longitude"]
                    address = pos["Result"]["Position"]["Address"]
                    pick_up = row.PickUp_H_Pos.split(",") 

                    file = self.configuration_api_google(status_detail, row, pick_up, now, lat, long)
                    
                    if file is not None:
                        print("Normal :::: - datetime : ", self.date_time()," - UID ",row.Uid," - Vehicule No :  ", row.vehicleno, " - Duration ", file["duration"], " - Distance ", file["distance"], " : ")
                        setattr(status_detail, 'uid', uid)
                        setattr(status_detail, 'coordonnee', f"{lat},{long}")
                        setattr(status_detail, 'current', address)
                        setattr(status_detail, 'idmere', status)
                        setattr(status_detail, 'duration', file["duration"])
                        setattr(status_detail, 'daty_time', now)
                        setattr(status_detail, 'id_trip', row.id_trip)
                        setattr(status_detail, 'distance', file["distance"])
                    
                    else:
                        print("Map error :::: - datetime : ", self.date_time()," - UID ",row.Uid," - Vehicule No :  ", row.vehicleno, " - Duration ", -1 , " - Distance ", 0, " : ")
                        setattr(status_detail, 'uid', uid)
                        setattr(status_detail, 'coordonnee', f"{lat},{long}")
                        setattr(status_detail, 'current', address)
                        setattr(status_detail, 'idmere', status)
                        setattr(status_detail, 'daty_time', now)
                        setattr(status_detail, 'id_trip', row.id_trip)
                        setattr(status_detail, 'duration', -1)
                        setattr(status_detail, 'distance', 0)
                        setattr(status_detail, 'daty_api_google', now)
                else:
                    print("Postion error :::: ", str(row.trip_start_date)+" "+ str(row.pick_up_time))
                    setattr(status_detail, 'uid', uid)
                    setattr(status_detail, 'coordonnee', "POSITION ERROR")
                    setattr(status_detail, 'current', "POSITION ERROR")
                    setattr(status_detail, 'idmere', status)
                    setattr(status_detail, 'daty_time', now)
                    setattr(status_detail, 'id_trip', row.id_trip)
                    setattr(status_detail, 'duration', -1)
                    setattr(status_detail, 'distance', 0)
            else:
                print("UID not found :::: ", str(row.trip_start_date)+" "+ str(row.pick_up_time))
                setattr(status_detail, 'uid', None)
                setattr(status_detail, 'coordonnee', "UID NOT FOUND")
                setattr(status_detail, 'current', "UID NOT FOUND")
                setattr(status_detail, 'idmere', status)
                setattr(status_detail, 'duration', 1)
                setattr(status_detail, 'daty_time', str(row.trip_start_date)+" "+ str(row.pick_up_time))
                setattr(status_detail, 'id_trip', row.id_trip)
                setattr(status_detail, 'distance', 0)
            status_detail.save()
        except Exception as e:
            raise e
        return status_detail
        
    def gestion_status_pos(self):
        status = Statuspos()
        self.count_sleep = 0
        try:
            list_uid = self.get_new_data()
            currentdate = self.date_time()
            now = currentdate
            date_time = now.strftime("%d %B %Y %H:%M:%S")
            setattr(status, 'datetime', now)
            setattr(status, 'desc', 'opp')
            setattr(status, 'nbre', len(list_uid))
            status.save()
            count = 1
            for row in list_uid:
                print(count,"/",len(list_uid))
                self.get_position_lat_long(row.Uid, date_time, row, status, now)    
                count = count + 1 
            self.add_log(now)
        except Exception as e:
            print(e)
            raise e
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
                        check[0].current = row.current
                        check[0].difftimestart = row.difftimestart
                        check[0].difftimepickup = row.difftimepickup
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
                    record.current = row.current
                    record.difftimestart = row.difftimestart
                    record.difftimepickup = row.difftimepickup
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
        liste = Recordcommenttrajet.objects.filter(daterecord__range = [dateinfrom,dateinto]).order_by('-daterecord','-actualtime')
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
    
    def save_data(self, ref):
        tab = []
        try:
            cursor = connections["asterix"].cursor()
            req = "SELECT t.vehicleno, t.driver_oname,t.driver_mobile_number,t.FromPlace,t.ToPlace,t.id_trip,t.`trip_no`,t.`trip_start_date`,t.`pick_up_time` AS pick_up_time,t.PickUp_H_Pos,t.resa_trans_type, t.gpsid FROM VW_GPSTracking t"
            cursor.execute(req)
            for row in cursor: 
                plan = planning()
                plan.save_trajetcoordonne(row, ref.id)   
                plan.save_planning(row, self.date_time())

            to_del = ref.id - 2
            Trajetcoordonnee.objects.filter(refresh_id__lte=to_del).delete()
        except Exception as e:
            raise e
            
    def rechange(self):
        try:
            self.api_units()
            #Trajetcoordonnee.objects.all().delete()
            ref = Refresh()
            ref.date_time = self.date_time()
            ref.save()
            self.save_data(ref)
        except Exception as e:
            raise e
        
    @transaction.atomic 
    def refresh(self):
        sid = transaction.savepoint()
        try:  
            self.get_api_data() 
            self.rechange()
            self.gestion_status_pos()
            transaction.savepoint_commit(sid)
        except Exception as e:
            print(e)
            transaction.savepoint_rollback(sid)
            raise e
        
    def getRecaprefresh(self, dateinfrom, dateinto):
        data = []
        if dateinfrom is None and dateinto is None:
            data =  Recaprefresh.objects.all()
        else:
            data = Recaprefresh.objects.filter(date__range = [dateinfrom,dateinto])
        return data
        
    