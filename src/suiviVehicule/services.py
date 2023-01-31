import pytz
import requests
from django.db import connection
from humanfriendly import format_timespan
from django.conf import settings
from suiviVehicule.models import Statuspos, UidName, Statusposdetail, Trajetcoordonnee, TrajetcoordonneeSamm
from datetime import datetime


class services():
    UserIdGuid = settings.USERIDGUID
    SessionId = settings.SESSIONID

    def get_api_data(self):
        response = requests.get(
            f'https://api.3dtracking.net/api/v1.0/Units/Unit/List?UserIdGuid={self.UserIdGuid}&SessionId={self.SessionId}')
        users = response.json()
        print("data ---- ", users)
        return False

    def get_position_at_time(self, uid, date_time):
        req = f"https://api.3dtracking.net/api/v1.0/Units/{uid}/PositionAtTime?UserIdGuid={self.UserIdGuid}&SessionId={self.SessionId}&PointInTimeDateTimeUTC={date_time}"
        response = requests.get(req)
        pos = response.json()
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
        result = requests.get(
            'https://maps.googleapis.com/maps/api/directions/json?',
            params={
                'origin': origin,
                'destination': destination,
                'waypoints': waypoints,
                "key": 'AIzaSyB2uvGCG5b8fsl9HD-hXW0GweGuBNzRM2U'
            })

        directions = result.json()
        # print("Direction ::: ",directions)
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
                    'distance': routes[route]["distance"]["text"],
                    'duration': routes[route]["duration"]["text"],

                    'steps': [
                        [
                            s["distance"]["text"],
                            s["duration"]["text"],
                            s["html_instructions"],

                        ]
                        for s in routes[route]["steps"]]
                }

                route_list.append(route_step)

        return {
            "origin": origin,
            "destination": destination,
            "distance": f"{round(distance / 1000, 2)} Km",
            "duration": duration
        }

    def set_one_refresh(self, idstatusdetail, id):
        data = Statusposdetail.objects.get(pk=idstatusdetail)
        trajet = Trajetcoordonnee.objects.get(pk=id)
        currentdate = datetime.now()
        print("--------- ", trajet.PickUp_H_Pos)
        date_time = currentdate.strftime("%d %B %Y %H:%M:%S")
        status_detail = self.get_position_lat_long(data.uid, date_time)
        file = self.get_direction(trajet.PickUp_H_Pos, status_detail.coordonnee)
        setattr(data, 'daty_time', currentdate)
        setattr(status_detail, 'duration', file["duration"])
        data.save()

    def gestion_status_pos(self):
        status = Statuspos()
        try:
            list_uid = self.get_data()
            currentdate = datetime.now()
            now = currentdate
            date_time = now.strftime("%d %B %Y %H:%M:%S")
            setattr(status, 'datetime', now)
            setattr(status, 'desc', 'opp')
            status.save()
            for row in list_uid:
                status_detail = self.get_position_lat_long(row.Uid, date_time)
                file = self.get_direction(row.PickUp_H_Pos, status_detail.coordonnee)
                print("UID ", row.Uid, "coordonnee 000 ", row.PickUp_H_Pos, " COORDONNEE 111 ",
                      status_detail.coordonnee)
                setattr(status_detail, 'idmere', status)
                setattr(status_detail, 'duration', file["duration"])
                setattr(status_detail, 'daty_time', now)
                status_detail.save()

        except Exception as e:
            print("error ", e)
        return status

    def get_last_refresh(self):
        data = []
        cursor = connection.cursor()
        cursor.execute(
            "select TIMESTAMPDIFF(second , datetime, current_timestamp()) as datetime From suiviVehicule_statuspos order by datetime asc")
        for row in cursor:
            data.append(row[0])
        return format_timespan(data[0])

    def get_data(self):
        data = TrajetcoordonneeSamm.objects.all().order_by('-trip_start_date', 'pick_up_time')
        trajetcoord = []
        for trajet in data:
            setattr(trajet, 'duration', str(trajet.duration))
            trajetcoord.append(trajet)
        return trajetcoord

    def get_data_search(self, form):
        data = TrajetcoordonneeSamm.objects.filter(driver_oname__icontains=form.cleaned_data['driver_oname'],
                                                   driver_mobile_number__icontains=form.cleaned_data[
                                                       'driver_mobile_number'],
                                                   vehicleno__icontains=form.cleaned_data['vehicleno'],
                                                   id_trip__icontains=form.cleaned_data['id_trip'],
                                                   FromPlace__icontains=form.cleaned_data['FromPlace'],
                                                   ToPlace__icontains=form.cleaned_data['ToPlace'],
                                                   status__icontains=form.cleaned_data['status'],
                                                   trip_no__icontains=form.cleaned_data['trip_no']).order_by(
            '-trip_start_date', 'pick_up_time')
        trajetcoord = []
        for trajet in data:
            setattr(trajet, 'duration', str(trajet.duration))
            trajetcoord.append(trajet)
        return trajetcoord

    def data_chart(self, data):
        label = []
        data = []
        couleur = []
        cursor = connection.cursor()
        req = "select sl.status , count(sl.status), sl.couleur from suiviVehicle_laststatus sl group by sl.status,sl.couleur"
        cursor.execute(req)
        for row in cursor:
            label.append(row[0])
            data.append(row[1])
            couleur.append(row[2])
        if len(data) == 0:
            return False
        return {
            "label": label,
            "data": data,
            "couleur": couleur
        }

    def data_chart_calcule(self, data):
        late = 0
        ontime = 0
        risky = 0
        terminated = 0
        label = ['Risky', 'On time', 'Terminated', 'Late']
        couleur = ['rgba(255,192,59,1.0)', 'rgba(30,132,127,1.0)', 'rgba(196,196,196,1.0)','rgba(255,110,64,1.0)']
        for row in data:
            if row.status == 'On time':
                ontime += 1
            elif row.status == 'Late':
                late += 1
            elif row.status == 'Risky':
                risky += 1
            elif row.status == 'Terminated':
                terminated += 1

        return {
            "label": label,
            "data": [risky, ontime, terminated, late],
            "couleur": couleur
        }
