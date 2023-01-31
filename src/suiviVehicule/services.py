from datetime import datetime, timezone

import pytz
import requests
from django.db import connection
from humanfriendly import format_timespan

from suiviVehicule.models import Statuspos, UidName, Statusposdetail, Trajetcoordonnee, TrajetcoordonneeSamm


class services():
    UserIdGuid = '3f55ba57-8a28-41cc-917d-718b9a754410'
    SessionId = '84a0d514-f64d-4220-b887-73186e8661c8'

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
        print("Direction ::: ",directions)
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
            now = datetime.now()
            #print("sitatut ", now.strftime("%d %B %Y %H:%M:%S"))
            date_time = now.strftime("%d %B %Y %H:%M:%S")
            setattr(status, 'datetime', now)
            setattr(status, 'desc', 'test')
            status.save()
            for row in list_uid:
                status_detail = self.get_position_lat_long(row.Uid, date_time)
                file = self.get_direction(row.coordonnee, status_detail.coordonnee)
                print("UID ", status_detail.uid, "coordonnee 000 ", row.coordonnee, " COORDONNEE 111 ",
                      status_detail.coordonnee)
                setattr(status_detail, 'idmere', status)
                setattr(status_detail, 'duration', file["duration"])
                setattr(status_detail, 'daty_time', now)
                status_detail.save()

        except Exception as e:
            print("error ", e)
        return status

    def get_join_table_trajetsummary(self):
        solution = []
        try:
            cursor = connection.cursor()
            cursor.execute("select Uid,vehicleno , PickUp_H_Pos  From suiviVehicule_trajetcoordonneesummary limit 10")
            for row in cursor:
                solution.append(UidName(row[1], row[0], row[2]))
        except Exception as e:
            print("error", str(e))
        finally:
            cursor.close()
        return solution

    def get_last_refresh(self):
        data = []
        cursor = connection.cursor()
        cursor.execute(
            "select TIMESTAMPDIFF(second , datetime, current_timestamp()) as datetime From suiviVehicule_statuspos order by datetime asc")
        for row in cursor:
            data.append(row[0])
        return format_timespan(data[0])

    def get_last_status(self):
        data = []
        cursor = connection.cursor()
        cursor.execute(
            "select id from suiviVehicule_statuspos where `datetime` = (select max(`datetime`) from suiviVehicule_statuspos ss )")
        for row in cursor:
            data.append(row[0])
        return data[0]

    def get_last_coordonneer(self, vehicleno):
        data = []
        idmere = self.get_last_status()
        cursor = connection.cursor()
        req = f"select * from suiviVehicule_getlastcoordonnee where idmere_id='{idmere}' and vehicleno='{vehicleno}'"
        cursor.execute(req)
        for row in cursor:
            data.append(row[3])
        if len(data) == 0:
            return False
        return data[0]

    def get_data(self):
        data = TrajetcoordonneeSamm.objects.all().order_by('-trip_start_date', 'pick_up_time')
        trajetcoord = []
        for trajet in data:
            setattr(trajet, 'duration', str(trajet.duration))
            trajetcoord.append(trajet)
        return trajetcoord

    def data_chart(self, data):
        label = []
        data = []
        couleur =[]
        cursor = connection.cursor()
        req = "select sl.status , count(sl.status), sl.couleur from suivivehicle_laststatus sl group by sl.status,sl.couleur"
        cursor.execute(req)
        for row in cursor:
            label.append(row[0])
            data.append(row[1])
            couleur.append(row[2])
        if len(data) == 0:
            return False
        return {
                "label": label,
                "data" : data,
                "couleur" : couleur
                }


