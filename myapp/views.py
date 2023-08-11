# from django.contrib.auth import authenticate
from allowances.auth import MyBackend
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from datetime import date

from .models import Users, Locations, Trips, Fuel_Prices

# from db_helper import *

backend = MyBackend.getInstance()


def index(request):
    if backend.get_active() == True:
        # Check for session persistence
        # ******************************
        # print("RETURNING TO HOME ", backend.rget_active())
        # ******************************

        return redirect("Home")
    return render(request, 'index.html')


@api_view(['POST'])
def Login(request):

    # Check for session persistence
    # ******************************
    # print("LOGIN RUNS ", backend.get_active())
    # ******************************

    if backend.get_active() == True:
        # Check for session persistence
        # ******************************
        # print("RETURNING TO HOME ", backend.get_active())
        # ******************************
        return redirect("Home")
    else:
        emp_id = request.POST.get("emp_id")
        emp_pass = request.POST.get("emp_pass")

        user = Users(emp_id, emp_pass)

        session_user = backend.authenticate(request, emp_id=emp_id, emp_pass=emp_pass)

        if session_user:
            print(session_user)
            # context = {
            #     "message": "Login successful"
            # }
            return redirect("Home")
            # return render(request, 'Home.html', context=context)
        else:
            # context = {
            #     "message": "Login failed"
            # }

            if not session_user:
                # Todo Lofin Failed Msg

                # return render(request, 'index.html', context=context)
                return redirect("Index")


@api_view(['POST'])
def Logout(request):
    backend.logout()
    return redirect("Index")


def Trans_req(request):
    if backend.get_active() is True:
        data = get_all_locations()
        LOV = {
            'Location_alias': data,
        }
        if request.method == 'POST':
            travel_from = request.POST.get("Travel_from")
            print(travel_from)
            travel_to = request.POST.get("Travel_To")
            Return_to = request.POST.get("Return_To")

            if travel_from == travel_to or travel_to == Return_to:
                LOV.update({'error_msg': backend.get_error_msg()['Trans_Req']})
                print(LOV['error_msg'])

            else:
                Emp_id = backend.get_current_logged_in()
                distance = 10
                last_updated_price = Fuel_Prices.objects.filter(fuel_type='PETROL').order_by('-fuel_date').first()

                if distance > 0 and last_updated_price.fuel_price > 0:
                    cost = (distance / 10) * last_updated_price.fuel_price
                else:
                    cost = 0

                Trip = Trips(travel_from=travel_from, travel_to=travel_to, emp_id=Emp_id, travel_return_to=Return_to,
                             travel_distance=distance, cost=cost, fuel=last_updated_price.fuel_price)
                Trip.save()

                LOV.update({'msg': backend.get_success()['Trans_Req']})
                print(LOV['msg'])

            return render(request, 'transRequest.html', context = LOV) #Todo Send Context
        else:
            return render(request, 'transRequest.html', context = LOV)
    else:
        return redirect("Index")
    # ------------------------------------------------------


def payment(request):
    if backend.get_active() == True:
        return render(request, 'allowances.html')
    else:
        return redirect("Index")


def Home(request):
    # print("OUTSIDE ACTIVE ACCOUNT: ", request.POST.get('travel_id'))
    if backend.get_active() == True:
        # print("INSIDE ACTIVE ACCOUNT: ",request.POST.get('travel_id'))
        travel_id = None
        travel_id = request.POST.get('travel_id')
        # print("Travel ID: ", travel_id)
        if travel_id:
            print('true')
            trip = Trips.objects.filter(emp_id=backend.get_current_logged_in(), travel_id=travel_id).values('travel_id',
                                                                                                            'travel_from',
                                                                                                            'travel_to',
                                                                                                            'travel_return_to',
                                                                                                            'travel_date'
                                                                                                            )
        else:
            # trip = 0
            trip = Trips.objects.filter(emp_id=backend.get_current_logged_in()).values('travel_id', 'travel_from',
                                                                                       'travel_to', 'travel_return_to','travel_date')

        print("Trips: ", trip)
        context = {
            "trips": trip,
        }
        # print("PRINTING CONTEXT:", end="")
        # print(context)

        return render(request, 'home.html', context=context)
    else:
        return redirect("Index")

def Add_Locations(request):
    if backend.get_active() == True:
        return render(request, 'add_location.html')
    else:
        return redirect("Index")


def get_all_locations():
    location: list
    location = Locations.objects.values_list('loc_name', flat=True)
    # Employees.objects.values_list('eng_name', flat=True)
    return location


@api_view(['POST'])
def location_save(request):

    if backend.get_active() is True:
        loc_alias = request.POST.get("Location_alias")
        loc_address = request.POST.get("Location_address")
        loc_check = Locations.objects.filter(loc_address = loc_address, loc_name =loc_alias, emp_id = backend.get_current_logged_in() )
        if not loc_check:
            loc = Locations(loc_name=loc_alias, loc_address=loc_address, emp_id = backend.get_current_logged_in())
            loc.save()
            return redirect('Transport_Request')
        else:

            return redirect('locations')
    else:
        return redirect("Index")


def plan_trip(request):

        return redirect('Home')


def add_petrol_price(request):
    if request.method == "POST":
        ft = request.POST.get("fuel_type")
        fpp = request.POST.get("fuel_price")
        fp = Fuel_Prices(fuel_price=fpp, fuel_type=ft)
        fp.save()
        return redirect("Transport_Request")
    else:
        return render(request, "add_petrol.html")


def history(request):
    currentMonth = date.today().replace(day=1)

    return render(request, "history.html")
