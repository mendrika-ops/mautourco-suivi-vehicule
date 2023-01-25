import requests


def get_direction():
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
