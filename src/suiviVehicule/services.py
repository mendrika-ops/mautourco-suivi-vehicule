from datetime import datetime, timezone

import requests
from django.db import connection
from humanfriendly import format_timespan

from suiviVehicule.models import Statuspos, UidName, Statusposdetail


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

    def get_direction(self):
        origin = '-20.302738,57.366069'
        destination = '-19.994282078890443,57.63655781308253'
        waypoints = '-20.302738,57.366069|-19.994282078890443,57.63655781308253'
        result = requests.get(
            'https://maps.googleapis.com/maps/api/directions/json?',
            params={
                'origin': origin,
                'destination': destination,
                'waypoints': waypoints,
                "key": 'AIzaSyB2uvGCG5b8fsl9HD-hXW0GweGuBNzRM2U'
            })

        directions = result.json()
        print(directions["routes"][0]["legs"])
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
            "duration": format_timespan(duration)
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

