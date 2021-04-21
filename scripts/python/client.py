from __future__ import print_function

import logging

import grpc

import ride_sharing_pb2
import ride_sharing_pb2_grpc

id_driver_list = []
driver_name_list = []
police_number_list = []
car_type_list = []
latitude_list = []
longitude_list = []
location_name_list = []
driver_rating_list = []
availability_list = []
distance_list = []
index_distance = 0


def user_data(stub, point):
    user = stub.GetUserLocation(point)
    if not user.location:
        print("Server Returned Incomplete feature")
        return
    if user.location_name:
        print("###########################################")
        print("User: {}".format(user.user_name))
        print("Location: {}".format(user.location_name))
        print("###########################################")
    else:
        print("Unidentified user at {}".format(user.location))


def locked_driver(stub):
    message1 = input("Continue Booking?(y/n): ")
    message1.lower()
    response = stub.BookingResponse(ride_sharing_pb2.MessageStream(text=message1))

    if message1 == "y":
        print("Server: {}".format(response.text))
        print("Driver name: {}".format(driver_name_list[index_distance]))
        print("Car Type: {}".format(car_type_list[index_distance]))
        print("Driver Location: {}".format(location_name_list[index_distance]))
        print("Driver Rating: {}".format(driver_rating_list[index_distance]))
        print("Distance to User: {} Km".format(round(distance_list[index_distance], 2)))
    elif message1 == "n":
        print("Server: {}".format(response.text))
        print("We will serve you another time....")
    else:
        print("Server: {}".format(response.text))


def guide_list_features(stub):
    rectangle = ride_sharing_pb2.Rectangle(
        lo=ride_sharing_pb2.Point(latitude=-7.0000000, longitude=100.0000000),
        hi=ride_sharing_pb2.Point(latitude=-6.0000000, longitude=110.0000000))
    print("Looking for features between -7 LS, 100 BB and -6 LS, 110 BB (Kota Bandung)")

    # initialize list for every element in feature

    features = stub.ListFeatures(rectangle)

    for feature in features:
        # printing driver data
        print("###########################################")
        print("Driver ID: {}".format(feature.id_driver))
        print("Driver name: {}".format(feature.driver_name))
        print("Car Type: {}".format(feature.car_type))
        print("Driver Latitude: {}".format(feature.location.latitude))
        print("Driver Longitude: {}".format(feature.location.longitude))
        print("Driver Location: {}".format(feature.location_name))
        print("Driver Rating: {}".format(feature.driver_rating))
        print("Driver Availability: {}".format(feature.availability))
        print("Distance to User: {} Km".format(round(feature.distance, 2)))
        print("###########################################")

        # adding data to list for sorting
        id_driver_list.append(feature.id_driver)
        driver_name_list.append(feature.driver_name)
        police_number_list.append(feature.police_number)
        car_type_list.append(feature.car_type)
        latitude_list.append(feature.location.latitude)
        longitude_list.append(feature.location.longitude)
        location_name_list.append(feature.location_name)
        driver_rating_list.append(feature.driver_rating)
        availability_list.append(feature.availability)
        distance_list.append(feature.distance)

    # finding shortest distance using min()
    shortest_distance = min(distance_list)

    # find another element in another list using index
    for i in range(0, len(distance_list)):
        if shortest_distance == distance_list[i]:
            global index_distance
            index_distance = i
    # print the detail of nearest driver
    print("-------------Nearest Driver--------------")
    print("###########################################")
    print("Driver ID: {}".format(id_driver_list[index_distance]))
    print("Driver name: {}".format(driver_name_list[index_distance]))
    print("Car Type: {}".format(car_type_list[index_distance]))
    print("Driver Latitude: {}".format(latitude_list[index_distance]))
    print("Driver Longitude: {}".format(longitude_list[index_distance]))
    print("Driver Location: {}".format(location_name_list[index_distance]))
    print("Driver Rating: {}".format(driver_rating_list[index_distance]))
    print("Driver Availability: {}".format(availability_list[index_distance]))
    print("Distance to User: {} Km".format(round(distance_list[index_distance], 2)))
    print("###########################################")


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = ride_sharing_pb2_grpc.RideSharingStub(channel)
        print("RONALDI RIDE SHARING")
        print("YOUR IDENTITY IS: ")
        print("----------------- User Data -----------------")
        user_data(stub, ride_sharing_pb2.Point(latitude=-6.95992390, longitude=107.6011345))
        print("OUR DRIVER LIST")
        print("----------------- List Driver --------------")
        guide_list_features(stub)
        print("--------------- Booking Form -------------")
        locked_driver(stub)


if __name__ == '__main__':
    logging.basicConfig()
    run()
