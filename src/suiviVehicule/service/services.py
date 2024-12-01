import pytz
import requests
from django.db import IntegrityError, connection, connections, transaction
from humanfriendly import format_timespan
from django.conf import settings
from suiviVehicule.models import *
from datetime import datetime,tzinfo
from dateutil import tz
import time
from suiviVehicule.planning import planning
from userManagement.service.twilio_service import send_trip_sms
from suiviVehicule.service.service_ia import IAService
from django.db.models import Sum, F, FloatField, ExpressionWrapper

class Services():
    UserIdGuid=''
    SessionId=''
    UserName = 'devvirmatics@mautourco.com'
    Password = 'Mautourco@1234'
    minvalue = 2
    maxvalue = 15
    count_sleep = 0

    def __init__(self) -> None:
        pass
    
    def get_api_data(self):
        response = requests.get(
            f'https://api.3dtracking.net/api/v1.0/Authentication/UserAuthenticate?UserName={self.UserName}&Password={self.Password}')
        users = response.json()
        self.UserIdGuid = users["Result"]["UserIdGuid"]
        self.SessionId = users["Result"]["SessionId"]
        print("User ID  = " +  self.UserIdGuid)
        print("Session ID = " + self.SessionId)
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
                setattr(units, 'Uid', result[i]["Uid"].strip())
                setattr(units, 'Name', result[i]["Name"].strip())
                setattr(units, 'IMEI', result[i]["IMEI"].strip())
                setattr(units, 'Status', result[i]["Status"])
                setattr(units, 'GroupName', result[i]["GroupName"])
                setattr(units, 'CompanyName', result[i]["CompanyName"])
                setattr(units, 'PhoneNumber', result[i]["PhoneNumber"])
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
        print("date time :  ", av)
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

    # def get_position_lat_long(self, uid, date_time, row, status, now):
    #     status_detail = Statusposdetail()
    #     file = []
    #     try:
    #         if uid is not None:
    #             pos = self.get_position_at_time(uid, date_time)

    #             if pos["Status"]["Result"] != 'Error':
    #                 lat = pos["Result"]["Position"]["Latitude"]
    #                 long = pos["Result"]["Position"]["Longitude"]
    #                 address = pos["Result"]["Position"]["Address"]
    #                 speed = pos["Result"]["Position"]["Speed"]
    #                 speedMeasure = pos["Result"]["Position"]["SpeedMeasure"]
    #                 odometer = pos["Result"]["Position"]["Odometer"]
    #                 ignition = pos["Result"]["Position"]["Ignition"]
    #                 engineTime = pos["Result"]["Position"]["EngineTime"]
    #                 engineStatus = pos["Result"]["Position"]["EngineStatus"]
    #                 pick_up = row.PickUp_H_Pos.split(",") 

    #                 file = self.configuration_api_google(status_detail, row, pick_up, now, lat, long)
                    
    #                 if file is not None:
    #                     print("Normal :::: - datetime : ", self.date_time()," - UID ",row.Uid," - Vehicule No :  ", row.vehicleno, " - Duration ", file["duration"], " - Distance ", file["distance"], " : ")
    #                     setattr(status_detail, 'uid', uid)
    #                     setattr(status_detail, 'coordonnee', f"{lat},{long}")
    #                     setattr(status_detail, 'current', address)
    #                     setattr(status_detail, 'idmere', status)
    #                     setattr(status_detail, 'duration', file["duration"])
    #                     setattr(status_detail, 'daty_time', now)
    #                     setattr(status_detail, 'id_trip', row.id_trip)
    #                     setattr(status_detail, 'distance', file["distance"])
                        
    #                     setattr(status_detail, 'speed', speed)
    #                     setattr(status_detail, 'speedMeasure', speedMeasure)
    #                     setattr(status_detail, 'odometer', odometer)
    #                     setattr(status_detail, 'ignition', ignition)
    #                     setattr(status_detail, 'engineTime', engineTime)
    #                     setattr(status_detail, 'engineStatus', engineStatus)
                    
    #                 else:
    #                     print("Map error :::: - datetime : ", self.date_time()," - UID ",row.Uid," - Vehicule No :  ", row.vehicleno, " - Duration ", -1 , " - Distance ", 0, " : ")
    #                     setattr(status_detail, 'uid', uid)
    #                     setattr(status_detail, 'coordonnee', f"{lat},{long}")
    #                     setattr(status_detail, 'current', address)
    #                     setattr(status_detail, 'idmere', status)
    #                     setattr(status_detail, 'daty_time', now)
    #                     setattr(status_detail, 'id_trip', row.id_trip)
    #                     setattr(status_detail, 'duration', -1)
    #                     setattr(status_detail, 'distance', 0)
    #                     setattr(status_detail, 'daty_api_google', now)

    #                     setattr(status_detail, 'speed', speed)
    #                     setattr(status_detail, 'speedMeasure', speedMeasure)
    #                     setattr(status_detail, 'odometer', odometer)
    #                     setattr(status_detail, 'ignition', ignition)
    #                     setattr(status_detail, 'engineTime', engineTime)
    #                     setattr(status_detail, 'engineStatus', engineStatus)
    #             else:
    #                 print("Postion error :::: ", str(row.trip_start_date)+" "+ str(row.pick_up_time))
    #                 setattr(status_detail, 'uid', uid)
    #                 setattr(status_detail, 'coordonnee', "POSITION ERROR")
    #                 setattr(status_detail, 'current', "POSITION ERROR")
    #                 setattr(status_detail, 'idmere', status)
    #                 setattr(status_detail, 'daty_time', now)
    #                 setattr(status_detail, 'id_trip', row.id_trip)
    #                 setattr(status_detail, 'duration', -1)
    #                 setattr(status_detail, 'distance', 0)
    #         else:
    #             print("UID not found :::: ", str(row.trip_start_date)+" "+ str(row.pick_up_time))
    #             setattr(status_detail, 'uid', None)
    #             setattr(status_detail, 'coordonnee', "UID NOT FOUND")
    #             setattr(status_detail, 'current', "UID NOT FOUND")
    #             setattr(status_detail, 'idmere', status)
    #             setattr(status_detail, 'duration', 1)
    #             setattr(status_detail, 'daty_time', str(row.trip_start_date)+" "+ str(row.pick_up_time))
    #             setattr(status_detail, 'id_trip', row.id_trip)
    #             setattr(status_detail, 'distance', 0)
    #         print("taste 1 ")
    #         status_detail.save()
    #         print("taste 2 ")
    #     except Exception as e:
    #         raise e
    #     return status_detail
    def get_position_lat_long(self, uid, date_time, row, status, now):
        status_detail = Statusposdetail()
        file = []
        default_duration = -1
        default_distance = 0

        def set_status_detail(lat=None, long=None, address=None, file=None, status=status, now=now, row=row):
            nonlocal status_detail
            coord = f"{lat},{long}" if lat and long else "POSITION ERROR"
            current = address if address else "POSITION ERROR"
            duration = file["duration"] if file else default_duration
            distance = file["distance"] if file else default_distance
            setattr(status_detail, 'uid', uid)
            setattr(status_detail, 'coordonnee', coord)
            setattr(status_detail, 'current', current)
            setattr(status_detail, 'idmere', status)
            setattr(status_detail, 'duration', duration)
            setattr(status_detail, 'distance', distance)
            setattr(status_detail, 'daty_time', now)
            setattr(status_detail, 'id_trip', row.id_trip)

        try:
            if uid is None:
                print(f"UID not found :::: {row.trip_start_date} {row.pick_up_time}")
                set_status_detail(coord="UID NOT FOUND", current="UID NOT FOUND", duration=1, now=f"{row.trip_start_date} {row.pick_up_time}")
            else:
                pos = self.get_position_at_time(uid, date_time)
                if pos["Status"]["Result"] != 'Error':
                    lat = pos["Result"]["Position"]["Latitude"]
                    long = pos["Result"]["Position"]["Longitude"]
                    address = pos["Result"]["Position"]["Address"]
                    speed = pos["Result"]["Position"]["Speed"]
                    speedMeasure = pos["Result"]["Position"]["SpeedMeasure"]
                    odometer = pos["Result"]["Position"]["Odometer"]
                    ignition = pos["Result"]["Position"]["Ignition"]
                    engineTime = pos["Result"]["Position"]["EngineTime"]
                    engineStatus = pos["Result"]["Position"]["EngineStatus"]
                    pick_up = row.PickUp_H_Pos.split(",")

                    file = self.configuration_api_google(status_detail, row, pick_up, now, lat, long)

                    if file:
                        print(f"Normal :::: - datetime : {self.date_time()} - UID {row.Uid} - Vehicle No: {row.vehicleno} - Duration {file['duration']} - Distance {file['distance']}")
                        set_status_detail(lat, long, address, file)
                    else:
                        print(f"Map error :::: - datetime : {self.date_time()} - UID {row.Uid} - Vehicle No: {row.vehicleno} - Duration -1 - Distance 0")
                        set_status_detail(lat, long, address)
                else:
                    print(f"Position error :::: {row.trip_start_date} {row.pick_up_time}")
                    set_status_detail()

            # Additional attributes for vehicle status
            if pos and pos["Status"]["Result"] != 'Error':
                setattr(status_detail, 'speed', pos["Result"]["Position"]["Speed"])
                setattr(status_detail, 'speedMeasure', pos["Result"]["Position"]["SpeedMeasure"])
                setattr(status_detail, 'odometer', 1.0)
                setattr(status_detail, 'ignition', pos["Result"]["Position"]["Ignition"])
                setattr(status_detail, 'engineTime', pos["Result"]["Position"]["EngineTime"])
                setattr(status_detail, 'engineStatus', pos["Result"]["Position"]["EngineStatus"])
            
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
            # status.save()
            count = 1
            for row in list_uid:
                print(count,"/",len(list_uid))
                # api get position google map
                # self.get_position_lat_long(row.Uid, date_time, row, status, now)
                data = Statusposdetail.objects.get(id_trip=row.id_trip)
                iaService = IAService()
                datapred = self.get_data_by_idtrip(row.id_trip)
                pred = iaService.loadModeleSupervisé(datapred)
                predict = [[float(value * 100) for value in sublist] for sublist in pred][0]
                print (predict[1])
                setattr(data, "annulated", predict[0])
                setattr(data, "risky", predict[1])
                setattr(data, "completed", predict[2])
                data.save()
                # send message
                self.set_trip_message(row)
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
    
    def get_listes_record(self,datefrom,dateto, status):
        dateinfrom = datetime. strptime(datefrom, '%Y-%m-%d')
        dateinto = datetime. strptime(dateto, '%Y-%m-%d')
        if status is not None:
            return Recordcommenttrajet.objects.filter(daterecord__range = [dateinfrom,dateinto], status__icontains=status).order_by('-daterecord','-actualtime')
        return Recordcommenttrajet.objects.filter(daterecord__range = [dateinfrom,dateinto]).order_by('-daterecord','-actualtime')
    
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
            # self.get_api_data() 
            # self.rechange()
            self.gestion_status_pos()
            transaction.savepoint_commit(sid)
        except Exception as e:
            print(e)
            transaction.savepoint_rollback(sid)
            raise e
        
    def getRecaprefresh(self, dateinfrom, dateinto):
       
        data = Recaprefresh.objects.filter(date__range = [dateinfrom,dateinto])
        return data
    
    def get_data_by_idtrip(self, id_trip):
        return TrajetcoordonneeVehicleInfo.objects.filter(id_trip=id_trip).first()
    
    def get_data_at_time(self):
        self.get_api_data()
        self.get_position_at_time("E39F3E", self.date_time())
        return
    
    def update_record_comment(self):
        self.get_api_data()
        posmin = StatusposMin.objects.all()[5000:10000]
        count = 0
        for ps in posmin:
            count+=1
            print(ps.uid, " - count ->", count)
            pos = self.get_position_at_time(ps.uid, ps.daty_time.strftime("%d %B %Y %H:%M:%S"))

            if pos["Status"]["Result"] != 'Error':
                speed = pos["Result"]["Position"]["Speed"]
                speedMeasure = pos["Result"]["Position"]["SpeedMeasure"]
                odometer = pos["Result"]["Position"]["Odometer"]
                ignition = pos["Result"]["Position"]["Ignition"]
                engineTime = pos["Result"]["Position"]["EngineTime"]
                engineStatus = pos["Result"]["Position"]["EngineStatus"]

                bank_position = BankPosition(
                    id_trip=ps.id_trip,
                    uid=ps.uid,  
                    daty_time=ps.daty_time,  
                    speed=speed,
                    speedMeasure=speedMeasure,
                    odometer=odometer,
                    ignition=ignition,
                    engineTime=engineTime,
                    engineStatus=engineStatus
                )

                print(
                    "Logger: id_trip : " + str(bank_position.id_trip) + " - " +
                    "uid : " + str(bank_position.uid) + " - " + 
                    "daty_time : " + str(bank_position.daty_time) + " - " +
                    "speed : " + str(bank_position.speed) + " - " +
                    "speedMeasure : " + str(bank_position.speedMeasure) + " - " +
                    "odometer : " + str(bank_position.odometer) + " - " +
                    "ignition : " + str(bank_position.ignition) + " - " +
                    "engineTime : " + str(bank_position.engineTime) + " - " +
                    "engineStatus : " + str(bank_position.engineStatus)
                )

                bank_position.save()
                print("Position enregistrée avec succès !")
            else:
                continue

    def update_vehicule_parameter(self):
        banks = BankPosition.objects.all()
        for bank in banks:
            record = Recordcomment.objects.filter(id_trip=bank.id_trip).first()
            if record:
                setattr(record, 'speed', bank.speed)
                setattr(record, 'speedMeasure', bank.speedMeasure)
                setattr(record, 'odometer', bank.odometer)
                setattr(record, 'ignition', bank.ignition)
                setattr(record, 'engineTime', bank.engineTime)
                setattr(record, 'engineStatus', bank.engineStatus)
                record.save()
                print(
                    "Logger: id_trip : " + str(record.id_trip) + " - " +
                    "speed : " + str(record.speed) + " - " +
                    "speedMeasure : " + str(record.speedMeasure) + " - " +
                    "odometer : " + str(record.odometer) + " - " +
                    "ignition : " + str(record.ignition) + " - " +
                    "engineTime : " + str(record.engineTime) + " - " +
                    "engineStatus : " + str(record.engineStatus)
                )
                print("Position enregistrée avec succès !")

    def update_vehicule_parameter_record(self):
        posBanks = StatusPosMinBank.objects.all()[0:1500]
        count = 0
        print("len ", len(posBanks))
        for pos in posBanks:
            plan = Planning.objects.filter(id_trip=pos.id_trip).first()
            if plan:
                count += 1
                record = Recordcomment()
                setattr(record, 'id_trip', pos.id_trip)
                setattr(record, 'comment', "transit-to-cancel")
                setattr(record, 'vehicleno', plan.vehicleno)
                setattr(record, 'driver_oname', plan.driver_oname)
                setattr(record, 'FromPlace', plan.FromPlace)
                setattr(record, 'ToPlace', plan.ToPlace)
                setattr(record, 'trip_start_date', plan.trip_start_date)
                setattr(record, 'pick_up_time', plan.pick_up_time)
                setattr(record, 'driver_mobile_number', plan.driver_mobile_number)
                setattr(record, 'datetime', pos.daty_time)
                setattr(record, 'etat', 0)
                setattr(record, 'difftimestart', 0)
                setattr(record, 'difftimepickup', 0)
                setattr(record, 'speed', pos.speed)
                setattr(record, 'speedMeasure', pos.speedMeasure)
                setattr(record, 'odometer', pos.odometer)
                setattr(record, 'ignition', pos.ignition)
                setattr(record, 'engineTime', pos.engineTime)
                setattr(record, 'engineStatus', pos.engineStatus)
                # record.save()
                print(
                    "Logger: id_trip : " + str(record.id_trip) + " - " +
                    "speed : " + str(record.speed) + " - " +
                    "speedMeasure : " + str(record.speedMeasure) + " - " +
                    "odometer : " + str(record.odometer) + " - " +
                    "ignition : " + str(record.ignition) + " - " +
                    "engineTime : " + str(record.engineTime) + " - " +
                    "engineStatus : " + str(record.engineStatus)
                )
                print("Bank :", len(posBanks))
                print("Position enregistrée avec succès ! -", count)
            else:
                print("Not in planning")
                continue

    def set_trip_message(self, trip):
        message = f"Hello {trip.driver_oname}, your trip from {trip.FromPlace} to {trip.ToPlace} is scheduled to start now. Please begin your journey and ensure arrival at {trip.ToPlace} by {trip.pick_up_time}. Drive safely!"
        driver_number = "+261341793201"
        tripMessageLib = TripMessageSendingLib.objects.filter(id_trip=trip.id_trip).exists()
        try:
            if not tripMessageLib:
                # send_trip_sms(driver_number, message)
                tripMessage = TripMessageSending()
                setattr(tripMessage, "name", "Begin trip Driver")
                setattr(tripMessage, "message", message)
                setattr(tripMessage, "id_trip", trip.id_trip)
                setattr(tripMessage, "is_send", True)
                tripMessage.save()
                print("message saved !")
        except Exception as e:
            #send notification 
            print(e)

    def get_trajet_performance_summary(self, start_date, end_date):
        summary = TrajetPerformanceSummary.objects.filter(
            trip_day__range=[start_date, end_date]
        ).aggregate(
            total_trips=Sum('total_trips'),
            completed_trips=Sum('completed_trips'),
            late_trips=Sum('late_trips'),
            canceled_trips=Sum('canceled_trips')
        )

        total_trips = summary['total_trips'] or 0
        summary['completed_percentage'] = round((summary['completed_trips'] * 100.0 / total_trips), 2) if total_trips > 0 else 0
        summary['late_percentage'] = round((summary['late_trips'] * 100.0 / total_trips), 2) if total_trips > 0 else 0
        summary['canceled_percentage'] = round((summary['canceled_trips'] * 100.0 / total_trips), 2) if total_trips > 0 else 0

        return summary
    
    def get_detail_info(self, id_trip):
        return TrajetDetailInfoVehicule.objects.filter(id_trip=id_trip).order_by('-daty_time')
    
    def get_rapportauto_list(self):
        return RapportAutoView.objects.all().order_by('-rapport_created_at')

    def get_rapportauto_log(self, id_report):
        return LogRapportAutoView.objects.filter(rapport_id=id_report)
            

                
        
        
    