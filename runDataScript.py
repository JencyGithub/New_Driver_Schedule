from Account_app.models import *
from GearBox_app.models import *
from django.utils import timezone 
import datetime

# ------------------------------
# Admin trucks
# ------------------------------


# trucks = [653, 654, 783, 784, 785, 786, 787, 782, 789, 550, 551, 552, 553, 554, 700, 701, 702, 703, 707, 708, 709, 719, 722, 723, 725, 726, 727, 728, 473, 470, 730, 471, 472, 731, 474, 475, 477]

# for truck in trucks:
#     try:
        
#         obj = AdminTruck(adminTruckNumber = truck)
#         obj.save()
#     except Exception as e:
#         print(f"Error : {e}")


# ------------------------------
# Client truck connection
# ------------------------------


def truckConnectionInsert(data):
    try:
        print(data['id'])
        adminTruckObj = AdminTruck.objects.get(pk = data['truckNumber'])
        rateCardObj = RateCard.objects.get(pk = data['rate_card_name'])
        clientObj = Client.objects.get(pk = data['clientId'])
        
        clientTruckConnectionObj = ClientTruckConnection(
            truckNumber =  adminTruckObj,
            truckType =  data['truckType'],
            rate_card_name =  rateCardObj,
            clientId =  clientObj,
            clientTruckId =  data['clientTruckId'],
            startDate =  data['startDate'],
            endDate =  data['endDate']
        )
        clientTruckConnectionObj.save()
        return
    except Exception as e :
        print(f'Load And Km Cost : {e}')
        return

connections = [
    {'id': 1, 'truckNumber': 37, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 477, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 2, 'truckNumber': 36, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 477, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 3, 'truckNumber': 35, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 474, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 4, 'truckNumber': 34, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 731, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 5, 'truckNumber': 33, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 472, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 6, 'truckNumber': 32, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 471, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 7, 'truckNumber': 31, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 730, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 8, 'truckNumber': 30, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 470, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 9, 'truckNumber': 29, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 473, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 10, 'truckNumber': 10, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 550, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 11, 'truckNumber': 11, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 551, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 12, 'truckNumber': 12, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 552, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 13, 'truckNumber': 13, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 553, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 14, 'truckNumber': 14, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 554, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 15, 'truckNumber': 1, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 653, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 16, 'truckNumber': 2, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 654, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 17, 'truckNumber': 15, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 700, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 18, 'truckNumber': 16, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 701, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 19, 'truckNumber': 17, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 702, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 20, 'truckNumber': 18, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 703, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 21, 'truckNumber': 19, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 707, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 22, 'truckNumber': 20, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 708, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 23, 'truckNumber': 21, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 709, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 24, 'truckNumber': 22, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 719, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 25, 'truckNumber': 23, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 722, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 26, 'truckNumber': 24, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 723, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 27, 'truckNumber': 25, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 725, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 28, 'truckNumber': 26, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 726, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 29, 'truckNumber': 27, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 727, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 30, 'truckNumber': 28, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 728, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 31, 'truckNumber': 8, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 782, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 32, 'truckNumber': 3, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 784, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 33, 'truckNumber': 4, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 784, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 34, 'truckNumber': 5, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 785, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 35, 'truckNumber': 6, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 786, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 36, 'truckNumber': 7, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 784, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 37, 'truckNumber': 9, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 789, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)},
    {'id': 38, 'truckNumber': 38, 'truckType': 'Embedded', 'rate_card_name': 2, 'clientId': 1, 'clientTruckId': 650, 'startDate': datetime.date(2023, 4, 1), 'endDate': datetime.date(2023, 4, 15)}
]

for connection in connections:
    truckConnectionInsert(connection)