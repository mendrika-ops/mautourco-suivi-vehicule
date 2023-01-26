from datetime import datetime, timezone

import requests
from django.db import connection
from humanfriendly import format_timespan

from suiviVehicule.models import Statuspos, UidName, Statusposdetail, Trajetcoordonnee


class services():
    UserIdGuid = '3f55ba57-8a28-41cc-917d-718b9a754410'
    SessionId = 'de70b2f5-c157-4e25-9456-620ec5c4e331'

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

    def gestion_status_pos(self):
        status = Statuspos()
        try:
            list_uid = self.get_join_table_trajetsummary()
            uid = '5CE7C3'
            date_time = '25 January 2023 07:14:00'
            now = datetime.now(timezone.utc)
            setattr(status, 'datetime', now)
            setattr(status, 'desc', 'ceci')
            status.save()
            for row in list_uid:
                status_detail = self.get_position_lat_long(row.Uid, date_time)
                print("UID ", status_detail.uid , " COORDONNEE ", status_detail.coordonnee)
                setattr(status_detail, 'idmere', status)
                status_detail.save()
            print("Status ---- ", status.id, status.datetime)

        except Exception as e:
            print("error ", e)
        return status

    def get_join_table_trajetsummary(self):
        solution = []
        try:
            cursor = connection.cursor()
            cursor.execute("select * From suivivehicule_trajetcoordonneesummary limit 10")
            for row in cursor:
                solution.append(UidName( row[1], row[0]))
        except Exception as e:
            print("error", str(e))
        finally:
            cursor.close()
        return solution

    def get_last_refresh(self):
        data = []
        cursor = connection.cursor()
        cursor.execute("select TIMESTAMPDIFF(second , datetime, UTC_TIMESTAMP()) as datetime From suivivehicule_statuspos order by datetime asc")
        for row in cursor:
            data.append(row[0])
        return format_timespan(data[0])

    def get_last_status(self):
        data = []
        cursor = connection.cursor()
        cursor.execute("select id from suivivehicule_statuspos where `datetime` = (select max(`datetime`) from suivivehicule_statuspos ss )")
        for row in cursor:
            data.append(row[0])
        return data[0]

    def get_last_coordonneer(self, vehicleno):
        data = []
        idmere = self.get_last_status()
        cursor = connection.cursor()
        req = f"select * from suivivehicule_getlastcoordonnee where idmere_id='{idmere}' and vehicleno='{vehicleno}'"
        print(req)
        cursor.execute(req)
        for row in cursor:
            print("LOOZZZAAAA ", row[3])
            data.append(row[3])
        if len(data) == 0:
            return False
        return data[0]

    def get_difference_date(self, duration, pick_up_time, trip_start_date):
        date = f'{trip_start_date} {str(pick_up_time)}'
        s = datetime.strptime(date, '%m/%d/%Y %H:%M:%S').timestamp()
        now = datetime.now(timezone.utc)
        prob = (now.timestamp() + duration)
        print("CALCULE ", prob, "SEC ", s)
        if prob == s:
            return "on time"
        elif prob > s:
            return "late"
        elif prob < s:
            return "Risky"
        elif duration == 0:
            return "cancel"

        print("duration : ", duration, "trip date ", str(prob))
    def get_data(self):
        data = Trajetcoordonnee.objects.all().order_by('-trip_start_date', '-pick_up_time')[0:10]
        trajetcoord = []
        for trajet in data:
            last = self.get_last_coordonneer(trajet.vehicleno)
            if last == False:
                setattr(trajet, 'PickEnd_H_Pos',trajet.PickUp_H_Pos)
            else:
                setattr(trajet, 'PickEnd_H_Pos', last)
            file = self.get_direction(trajet.PickEnd_H_Pos, trajet.PickUp_H_Pos)
            calcdate = self.get_difference_date(file["duration"], trajet.pick_up_time, trajet.trip_start_date)
            setattr(trajet, 'status', calcdate)
            setattr(trajet, 'duration', format_timespan(file["duration"]))

            print("Stat ", trajet.status)
            trajetcoord.append(trajet)
        return trajetcoord



