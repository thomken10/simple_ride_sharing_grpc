from concurrent import futures

from math import cos, sin, asin, sqrt, radians

import logging

import grpc

import ride_sharing_pb2
import ride_sharing_pb2_grpc
import json_load


def get_user(user_db, point):
    for user in user_db:
        if user.location == point:
            return user
    return None


def get_distance(start, end):
    lat_rad_1 = radians(start.latitude)
    lat_rad_2 = radians(end.latitude)
    delta_lat_rad = radians(end.latitude - start.latitude)
    delta_lon_rad = radians(end.longitude - start.longitude)

    # Formula is based on http://mathforum.org/library/drmath/view/51879.html
    a = sin(delta_lat_rad / 2) ** 2 + cos(lat_rad_1) * cos(lat_rad_2) * sin(delta_lon_rad / 2) ** 2
    c = 2 * asin(sqrt(a))
    R = 6371
    distance = R * c
    # radius in kilometres
    return distance


class RideSharingServicer(ride_sharing_pb2_grpc.RideSharingServicer):

    def __init__(self):
        self.db_driver = json_load.load_json_driver()
        self.db_user = json_load.load_json_user()

    def GetUserLocation(self, request, context):
        user = get_user(self.db_user, request)
        if user is None:
            return ride_sharing_pb2.User(id_user="", user_name="", location_name="", location=request)
        else:
            return user

    def ListFeatures(self, request, context):
        left = min(request.lo.longitude, request.hi.longitude)
        right = max(request.lo.longitude, request.hi.longitude)
        top = max(request.lo.latitude, request.hi.latitude)
        bottom = min(request.lo.latitude, request.hi.latitude)

        for user in self.db_user:
            for feature in self.db_driver:
                if (left <= feature.location.longitude <= right
                        and bottom <= feature.location.latitude <= top):
                    feature.distance = get_distance(user.location, feature.location)
                    yield feature

    def FinishedBooking(self, request, context):
        if request.text == "y":
            message = "Trip Completed, please rate the driver"
        elif request.text == "n":
            message = "Sorry to know, please give us feedback"
        else:
            message = "Choose the right Input!!"
        return ride_sharing_pb2.MessageResponse(text=message)

    def BookingResponse(self, request, context):
        if request.text == "y":
            message = "Booking Completed!"
        elif request.text == "n":
            message = "Booking Aborted!"
        else:
            message = "Choose the right Input!!"
        return ride_sharing_pb2.MessageResponse(text=message)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ride_sharing_pb2_grpc.add_RideSharingServicer_to_server(RideSharingServicer(), server)
    print("Server Listening 50051")
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
