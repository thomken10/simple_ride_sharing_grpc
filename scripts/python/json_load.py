import json
import ride_sharing_pb2


def load_json_driver():
    driver_list = []
    with open("driver_db.json") as driver_db_file:
        for item in json.load(driver_db_file):
            feature = ride_sharing_pb2.Feature(
                id_driver=item["id_driver"],
                driver_name=item["driver_name"],
                police_number=item["police_number"],
                car_type=item["car_type"],
                location=ride_sharing_pb2.Point(latitude=item["location"]["latitude"],
                                                longitude=item["location"]["longitude"]),
                location_name=item["location_name"],
                driver_rating=item["driver_rating"],
                availability=item["availability"]
            )
            driver_list.append(feature)
    return driver_list


def load_json_user():
    user_list = []
    with open("user.json") as user_db_file:
        for item in json.load(user_db_file):
            user = ride_sharing_pb2.User(
                id_user=item["id_user"],
                user_name=item["user_name"],
                location=ride_sharing_pb2.Point(latitude=item["location"]["latitude"],
                                                longitude=item["location"]["longitude"]),
                location_name=item["location_name"]
            )
        user_list.append(user)
    return user_list

# if __name__ == '__main__':
#     # load_json_driver()
#     load_json_user()
