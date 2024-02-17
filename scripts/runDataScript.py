from Account_app.models import *
from GearBox_app.models import *
from django.utils import timezone 
import datetime

# # ------------------------------
# # Admin trucks
# # ------------------------------


# # trucks = [653, 654, 783, 784, 785, 786, 787, 782, 789, 550, 551, 552, 553, 554, 700, 701, 702, 703, 707, 708, 709, 719, 722, 723, 725, 726, 727, 728, 473, 470, 730, 471, 472, 731,
# #           474, 475, 477]
trucks = [
    {'id': 56, 'adminTruckNumber': 1100, 'truckStatus': False},
    {'id': 57, 'adminTruckNumber': 1154, 'truckStatus': False},
    {'id': 58, 'adminTruckNumber': 1160, 'truckStatus': False},
    {'id': 59, 'adminTruckNumber': 1164, 'truckStatus': False},
    {'id': 60, 'adminTruckNumber': 1186, 'truckStatus': False},
    {'id': 61, 'adminTruckNumber': 1463, 'truckStatus': False},
    {'id': 62, 'adminTruckNumber': 2238, 'truckStatus': False},
    {'id': 63, 'adminTruckNumber': 2281, 'truckStatus': False},
    {'id': 64, 'adminTruckNumber': 2282, 'truckStatus': False},
    {'id': 65, 'adminTruckNumber': 2283, 'truckStatus': False},
    {'id': 66, 'adminTruckNumber': 2285, 'truckStatus': False},
    {'id': 67, 'adminTruckNumber': 2293, 'truckStatus': False},
    {'id': 68, 'adminTruckNumber': 2294, 'truckStatus': False},
    {'id': 69, 'adminTruckNumber': 2295, 'truckStatus': False},
    {'id': 70, 'adminTruckNumber': 2296, 'truckStatus': False},
    {'id': 71, 'adminTruckNumber': 2297, 'truckStatus': False},
    {'id': 72, 'adminTruckNumber': 2322, 'truckStatus': False},
    {'id': 73, 'adminTruckNumber': 2330, 'truckStatus': False},
    {'id': 74, 'adminTruckNumber': 2332, 'truckStatus': False},
    {'id': 75, 'adminTruckNumber': 2333, 'truckStatus': False},
    {'id': 76, 'adminTruckNumber': 2358, 'truckStatus': False},
    {'id': 77, 'adminTruckNumber': 2365, 'truckStatus': False},
    {'id': 78, 'adminTruckNumber': 2373, 'truckStatus': False},
    {'id': 79, 'adminTruckNumber': 2376, 'truckStatus': False},
    {'id': 80, 'adminTruckNumber': 2455, 'truckStatus': False},
    {'id': 81, 'adminTruckNumber': 2656, 'truckStatus': False},
    {'id': 82, 'adminTruckNumber': 2670, 'truckStatus': False},
    {'id': 83, 'adminTruckNumber': 2671, 'truckStatus': False},
    {'id': 84, 'adminTruckNumber': 2672, 'truckStatus': False},
    {'id': 85, 'adminTruckNumber': 2673, 'truckStatus': False},
    {'id': 86, 'adminTruckNumber': 2674, 'truckStatus': False},
    {'id': 87, 'adminTruckNumber': 2675, 'truckStatus': False},
    {'id': 88, 'adminTruckNumber': 2677, 'truckStatus': False},
    {'id': 89, 'adminTruckNumber': 2680, 'truckStatus': False},
    {'id': 90, 'adminTruckNumber': 2683, 'truckStatus': False},
    {'id': 91, 'adminTruckNumber': 2687, 'truckStatus': False},
    {'id': 92, 'adminTruckNumber': 2689, 'truckStatus': False},
    {'id': 93, 'adminTruckNumber': 2692, 'truckStatus': True},
    {'id': 94, 'adminTruckNumber': 2693, 'truckStatus': True},
    {'id': 95, 'adminTruckNumber': 2694, 'truckStatus': False},
    {'id': 96, 'adminTruckNumber': 2695, 'truckStatus': False},
    {'id': 97, 'adminTruckNumber': 2696, 'truckStatus': False},
    {'id': 98, 'adminTruckNumber': 2742, 'truckStatus': False},
    {'id': 99, 'adminTruckNumber': 2743, 'truckStatus': False},
    {'id': 100, 'adminTruckNumber': 2746, 'truckStatus': False},
    {'id': 101, 'adminTruckNumber': 2828, 'truckStatus': False},
    {'id': 102, 'adminTruckNumber': 2829, 'truckStatus': False},
    {'id': 103, 'adminTruckNumber': 2944, 'truckStatus': False},
    {'id': 104, 'adminTruckNumber': 2954, 'truckStatus': False},
    {'id': 105, 'adminTruckNumber': 2955, 'truckStatus': False},
    {'id': 106, 'adminTruckNumber': 3188, 'truckStatus': False},
    {'id': 107, 'adminTruckNumber': 3417, 'truckStatus': False},
    {'id': 108, 'adminTruckNumber': 3418, 'truckStatus': False},
    {'id': 109, 'adminTruckNumber': 3420, 'truckStatus': False},
    {'id': 110, 'adminTruckNumber': 3423, 'truckStatus': False},
    {'id': 111, 'adminTruckNumber': 3424, 'truckStatus': False},
    {'id': 112, 'adminTruckNumber': 3425, 'truckStatus': False},
    {'id': 113, 'adminTruckNumber': 3432, 'truckStatus': False},
    {'id': 114, 'adminTruckNumber': 4259, 'truckStatus': False},
    {'id': 115, 'adminTruckNumber': 4260, 'truckStatus': False},
    {'id': 116, 'adminTruckNumber': 4261, 'truckStatus': False},
    {'id': 117, 'adminTruckNumber': 4265, 'truckStatus': False},
    {'id': 118, 'adminTruckNumber': 4367, 'truckStatus': False},
    {'id': 119, 'adminTruckNumber': 4381, 'truckStatus': False},
    {'id': 120, 'adminTruckNumber': 4382, 'truckStatus': False},
    {'id': 121, 'adminTruckNumber': 4636, 'truckStatus': False},
    {'id': 122, 'adminTruckNumber': 4637, 'truckStatus': False},
    {'id': 123, 'adminTruckNumber': 4638, 'truckStatus': False},
    {'id': 124, 'adminTruckNumber': 4639, 'truckStatus': False},
    {'id': 125, 'adminTruckNumber': 4640, 'truckStatus': False},
    {'id': 126, 'adminTruckNumber': 4642, 'truckStatus': False},
    {'id': 127, 'adminTruckNumber': 4679, 'truckStatus': False},
    {'id': 128, 'adminTruckNumber': 4680, 'truckStatus': False},
    {'id': 129, 'adminTruckNumber': 4734, 'truckStatus': False},
    {'id': 130, 'adminTruckNumber': 6063, 'truckStatus': False},
    {'id': 131, 'adminTruckNumber': 6591, 'truckStatus': False},
    {'id': 132, 'adminTruckNumber': 6592, 'truckStatus': True},
    {'id': 133, 'adminTruckNumber': 6593, 'truckStatus': True},
    {'id': 134, 'adminTruckNumber': 6594, 'truckStatus': False},
    {'id': 135, 'adminTruckNumber': 6596, 'truckStatus': False},
    {'id': 136, 'adminTruckNumber': 8200, 'truckStatus': False},
    {'id': 137, 'adminTruckNumber': 8201, 'truckStatus': False},
    {'id': 138, 'adminTruckNumber': 8603, 'truckStatus': False},
    {'id': 139, 'adminTruckNumber': 8604, 'truckStatus': False},
    {'id': 140, 'adminTruckNumber': 8681, 'truckStatus': False},
    {'id': 141, 'adminTruckNumber': 8683, 'truckStatus': False},
    {'id': 142, 'adminTruckNumber': 9114, 'truckStatus': False},
    {'id': 143, 'adminTruckNumber': 9115, 'truckStatus': False},
    {'id': 144, 'adminTruckNumber': 9140, 'truckStatus': True},


]

for truck in trucks:
    try:
        
        obj = AdminTruck(id =  truck['id'], adminTruckNumber = truck['adminTruckNumber'], truckActive = truck['truckStatus'], createdBy=User.objects.filter().first())
        # obj = AdminTruck(adminTruckNumber = truck)
        obj.save()
    except Exception as e:
        print(f"Error : {e}")


# # ------------------------------
# # Client truck connection
# # ------------------------------


def truckConnectionInsert(data):
    try:
        # print(data['id'])
        adminTruckObj = AdminTruck.objects.get(pk = data['truckNumber'])
        # rateCardObj = RateCard.objects.filter(pk=data['rate_card_name']).first()
        rateCardObj = RateCard.objects.filter().first()
        clientObj = Client.objects.get(pk = data['clientId'])
        
        clientTruckConnectionObj = ClientTruckConnection(
            truckNumber =  adminTruckObj,
            truckType =  data['truckType'],
            rate_card_name =  rateCardObj,
            clientId =  clientObj,
            clientTruckId =  data['clientTruckId'],
            startDate =  data['startDate'],
            endDate =  data['endDate'],
            createdBy=User.objects.filter().first()
        )
        clientTruckConnectionObj.save()
        return
    except Exception as e :
        print(f'Error Truck Number :, {e}')
        return
    




connections = [  
{'id': 743, 'truckNumber': 56, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 1100, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 744, 'truckNumber': 57, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 1154, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 745, 'truckNumber': 58, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 1160, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 746, 'truckNumber': 59, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 1164, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 747, 'truckNumber': 60, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 1186, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 748, 'truckNumber': 61, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 1463, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 749, 'truckNumber': 62, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2238, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 750, 'truckNumber': 63, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2281, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 751, 'truckNumber': 64, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2282, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 752, 'truckNumber': 65, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2283, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 753, 'truckNumber': 66, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2285, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 754, 'truckNumber': 67, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2293, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 755, 'truckNumber': 68, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2294, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 756, 'truckNumber': 69, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2295, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 757, 'truckNumber': 70, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2296, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 758, 'truckNumber': 71, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2297, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 759, 'truckNumber': 72, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2322, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 760, 'truckNumber': 73, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2330, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 761, 'truckNumber': 74, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2332, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 762, 'truckNumber': 75, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2333, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 763, 'truckNumber': 76, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2358, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 764, 'truckNumber': 77, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2365, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 765, 'truckNumber': 78, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2373, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 766, 'truckNumber': 79, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2376, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 767, 'truckNumber': 80, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2455, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 768, 'truckNumber': 81, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2656, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 769, 'truckNumber': 82, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2670, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 770, 'truckNumber': 83, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2671, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 771, 'truckNumber': 84, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2672, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 772, 'truckNumber': 85, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2673, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 773, 'truckNumber': 86, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2674, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 774, 'truckNumber': 87, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2675, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 775, 'truckNumber': 88, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2677, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 776, 'truckNumber': 89, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2680, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 777, 'truckNumber': 90, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2683, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 778, 'truckNumber': 91, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2687, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 779, 'truckNumber': 92, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2689, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 780, 'truckNumber': 93, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2692, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 781, 'truckNumber': 94, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2693, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 782, 'truckNumber': 95, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2694, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 783, 'truckNumber': 96, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2695, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 784, 'truckNumber': 97, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2696, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 785, 'truckNumber': 98, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2742, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
 {'id': 786, 'truckNumber': 99, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2743, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 787, 'truckNumber': 100, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2746, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 788, 'truckNumber': 101, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2828, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 789, 'truckNumber': 102, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2829, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 790, 'truckNumber': 103, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2944, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 791, 'truckNumber': 104, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2954, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 792, 'truckNumber': 105, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 2955, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 793, 'truckNumber': 106, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 3188, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 794, 'truckNumber': 107, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 3417, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 795, 'truckNumber': 108, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 3418, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 796, 'truckNumber': 109, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 3420, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 797, 'truckNumber': 110, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 3423, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 798, 'truckNumber': 111, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 3424, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 799, 'truckNumber': 112, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 3425, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 800, 'truckNumber': 113, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 3432, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 801, 'truckNumber': 114, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 4259, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 802, 'truckNumber': 115, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 4260, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 803, 'truckNumber': 116, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 4261, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 804, 'truckNumber': 117, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 4265, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 805, 'truckNumber': 118, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 4367, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 806, 'truckNumber': 119, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 4381, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 807, 'truckNumber': 120, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 4382, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 808, 'truckNumber': 121, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 4636, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 809, 'truckNumber': 122, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 4637, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 810, 'truckNumber': 123, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 4638, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 811, 'truckNumber': 124, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 4639, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 812, 'truckNumber': 125, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 4640, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 813, 'truckNumber': 126, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 4642, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 814, 'truckNumber': 127, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 4679, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 815, 'truckNumber': 128, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 4680, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 816, 'truckNumber': 129, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 4734, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 817, 'truckNumber': 130, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 6063, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 818, 'truckNumber': 131, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 6591, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 819, 'truckNumber': 132, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 6592, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 820, 'truckNumber': 133, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 6593, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 821, 'truckNumber': 134, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 6594, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 822, 'truckNumber': 135, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 6596, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 823, 'truckNumber': 136, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 8200, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 824, 'truckNumber': 137, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 8201, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 825, 'truckNumber': 138, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 8603, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 826, 'truckNumber': 139, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 8604, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 827, 'truckNumber': 140, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 8681, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 828, 'truckNumber': 141, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 8683, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 829, 'truckNumber': 142, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 9114, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 830, 'truckNumber': 143, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 9115, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
{'id': 831, 'truckNumber': 144, 'truckType': 'Embedded','rate_card_name': 1,'clientId': 2, 'clientTruckId': 9140, 'startDate': datetime.date(2023, 1, 1), 'endDate': datetime.date(2023, 12, 30)},
    ]


for connection in connections:
    truckConnectionInsert(connection)
basePlant = [
    {'basePlant':'ALBION PARK', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 171.0120 , 'long': 172.1510},
    {'basePlant':'ALEXANDRIA', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 170.0120 , 'long': 173.1510},
    {'basePlant':'ARDEN', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 169.0120 , 'long': 174.1510},
    {'basePlant':'ARTARMON', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 168.0120 , 'long': 175.1510},
    {'basePlant':'BASS', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 167.0120 , 'long': 176.1510},
    {'basePlant':'BAYSWATER', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 166.0120 , 'long': 177.1510},
    {'basePlant':'BAYSWATER (B&F) TOLLING', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 165.0120 , 'long': 178.1510},
    {'basePlant':'BIBRA LAKE', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 164.0120 , 'long': 179.1510},
    {'basePlant':'BLACKTOWN', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 163.0120 , 'long': 180.1510},
    {'basePlant':'BROMPTON', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 162.0120 , 'long': 181.1510},
    {'basePlant':'BROOKVALE', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 161.0120 , 'long': 182.1510},
    {'basePlant':'CAMELLIA', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 160.0120 , 'long': 183.1510},
    {'basePlant':'CARINGBAH', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 159.0120 , 'long': 184.1510},
    {'basePlant':'DROUIN', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 158.0120 , 'long': 185.1510},
    {'basePlant':'EAST PERTH', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 157.0120 , 'long': 186.1510},
    {'basePlant':'ELIZABETH MOBILE', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 156.0120 , 'long': 187.1510},
    {'basePlant':'EMU PLAINS', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 155.0120 , 'long': 188.1510},
    {'basePlant':'EMU PLAINS (TOLL)', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 154.0120 , 'long': 189.1510},
    {'basePlant':'EPPING', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 153.0120 , 'long': 190.1510},
    {'basePlant':'FOOTSCRAY', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 152.0120 , 'long': 191.1510},
    {'basePlant':'FOOTSCRAY (B&F) TOLL', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 151.0120 , 'long': 192.1510},
    {'basePlant':'GEELONG', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 150.0120 , 'long': 193.1510},
    {'basePlant':'GNANGARA', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 149.0120 , 'long': 194.1510},
    {'basePlant':'HASTINGS', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 148.0120 , 'long': 195.1510},
    {'basePlant':'HEATHERBRAE', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 147.0120 , 'long': 196.1510},
    {'basePlant':'HORNSBY', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 146.0120 , 'long': 197.1510},
    {'basePlant':'JEERALANG', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 145.0120 , 'long': 198.1510},
    {'basePlant':'KEILOR', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 144.0120 , 'long': 199.1510},
    {'basePlant':'LANG LANG', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 143.0120 , 'long': 200.1510},
    {'basePlant':'LAVERTON', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 142.0120 , 'long': 201.1510},
    {'basePlant':'LAVERTON (B&F) TOLLING', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 141.0120 , 'long': 202.1510},
    {'basePlant':'LIDCOMBE', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 140.0120 , 'long': 203.1510},
    {'basePlant':'LIVERPOOL', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 139.0120 , 'long': 204.1510},
    {'basePlant':'LONSDALE', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 138.0120 , 'long': 205.1510},
    {'basePlant':'LYNDHURST', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 137.0120 , 'long': 206.1510},
    {'basePlant':'LYNDHURST (B&F) TOLL', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 136.0120 , 'long': 207.1510},
    {'basePlant':'Lynwood', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 135.0120 , 'long': 208.1510},
    {'basePlant':'MACKAY', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 134.0120 , 'long': 209.1510},
    {'basePlant':'MANNINGHAM', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 133.0120 , 'long': 210.1510},
    {'basePlant':'Manor', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 132.0120 , 'long': 211.1510},
    {'basePlant':'MANOR QUARRY', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 131.0120 , 'long': 212.1510},
    {'basePlant':'Moriac', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 130.0120 , 'long': 213.1510},
    {'basePlant':'MORIAC SAND', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 129.0120 , 'long': 214.1510},
    {'basePlant':'NARELLAN', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 128.0120 , 'long': 215.1510},
    {'basePlant':'NEBO', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 127.0120 , 'long': 216.1510},
    {'basePlant':'Oaklands', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 126.0120 , 'long': 217.1510},
    {'basePlant':'OAKLANDS JUNCTION', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 125.0120 , 'long': 218.1510},
    {'basePlant':'PAKENHAM', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 124.0120 , 'long': 219.1510},
    {'basePlant':'PAKENHAM (B&F) TOLLING', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 123.0120 , 'long': 220.1510},
    {'basePlant':'PAKENHAM QUARRY', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 122.0120 , 'long': 221.1510},
    {'basePlant':'PENDLE HILL', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 121.0120 , 'long': 222.1510},
    {'basePlant':'PRESTON', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 120.0120 , 'long': 223.1510},
    {'basePlant':'PRESTON (B&F) TOLL', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 119.0120 , 'long': 224.1510},
    {'basePlant':'ROCKINGHAM', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 118.0120 , 'long': 225.1510},
    {'basePlant':'ROOTY HILL', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 117.0120 , 'long': 226.1510},
    {'basePlant':'ROSEBUD', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 116.0120 , 'long': 227.1510},
    {'basePlant':'ROSEBUD (B&F) TOLL', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 115.0120 , 'long': 228.1510},
    {'basePlant':'SARINA', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 114.0120 , 'long': 229.1510},
    {'basePlant':'SEAFORD', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 113.0120 , 'long': 230.1510},
    {'basePlant':'SEAFORD (B&F) TOLLING', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 112.0120 , 'long': 231.1510},
    {'basePlant':'SPRINGVALE', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 111.0120 , 'long': 232.1510},
    {'basePlant':'SPRINGVALE (B & F) CONC', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 110.0120 , 'long': 233.1510},
    {'basePlant':'TRUGANINA (TOLL)', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 109.0120 , 'long': 234.1510},
    {'basePlant':'Tynong', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 108.0120 , 'long': 235.1510},
    {'basePlant':'TYNONG QUARRY', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 107.0120 , 'long': 236.1510},
    {'basePlant':'WANNEROO', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 106.0120 , 'long': 237.1510},
    {'basePlant':'WELSHPOOL', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 105.0120 , 'long': 238.1510},
    {'basePlant':'Werribee', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 104.0120 , 'long': 239.1510},
    {'basePlant':'WEST SYD AIRPORT MOBILE CONC #6', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 103.0120 , 'long': 240.1510},
    {'basePlant':'WETHERILL PARK', 'address':'xyz' , 'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 102.0120 , 'long': 241.1510},
    {'basePlant':'WOLLERT (B&F) TOLLING','address':'xyz' ,'phone':112345679 , 'personName':'abc','managerName':'dce','lat': 101.0120 , 'long': 242.1510}
]

for data in basePlant:
    try:
        obj = BasePlant()
        obj.basePlant = data['basePlant'] 
        obj.address = data['address']
        obj.phone = data['phone']
        obj.personName = data['personName']
        obj.managerName = data['managerName']
        obj.lat = data['lat']
        obj.long = data['long']
        obj.save()
    except Exception as e:
        print("Error:",str(data))
    
# def run():
#     data = ClientTruckConnection.objects.all().values()

#     with open('pastTrip_entry.txt','a') as f:
        
#         for i in data:
#             f.write('\n' + str(i))
    