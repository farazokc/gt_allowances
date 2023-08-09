from django.shortcuts import render, HttpResponse,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Users, Locations, Trips, Fuel_Prices
# from django.contrib.auth import authenticate
from allowances.auth import MyBackend
# from db_helper import *

backend = MyBackend.getInstance()

def index(request):
    if backend.get_active() == True:
        # Check for session persistence
        # ******************************
        # print("RETURNING TO HOME ", backend.get_active())
        # ******************************

        return redirect("Home")
    return render(request, 'index.html')

@api_view(['POST'])
def Login(request):
    request.session['loginMsg'] = None
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

        session_user = backend.authenticate(request,emp_id=emp_id,emp_pass=emp_pass)

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
                if 'loginMsg' in request.session:
                    del request.session['loginMsg']

                request.session['loginMsg'] = "ID or Password is incorrect"
                print("MESSAGE:" + request.session['loginMsg'])

                # return render(request, 'index.html', context=context)
                return redirect("Index")

@api_view(['POST'])
def Logout(request):
    backend.logout()
    return redirect("Index")

def Trans_req(request):
    data = get_all_locations()
    context = {
        'Location_alias' : data
    }
    if backend.get_active() is True:
        return render(request, 'transRequest.html', context= context)
    else:
        return redirect("Index")


def payment(request):
    if backend.get_active() == True:
        return render(request, 'allowances.html')
    else:
        return redirect("Index")


def Home(request):
    if backend.get_active() == True:
        
        # get and print
        travel_id = request.POST.get('travel_id')
        if travel_id:
            trip = Trips.objects.filter(emp_id = backend.get_current_logged_in(), travel_id = travel_id ).values('travel_id', 'travel_from', 'travel_to', 'travel_return_to')
        else:
            trip = Trips.objects.filter(emp_id = backend.get_current_logged_in() ).values('travel_id', 'travel_from', 'travel_to', 'travel_return_to')
        
        

        context = {
            "trips": trip,
        }
        print(context)

        return render(request, 'home.html', context=context)
    else:
        return redirect("Index")

# def test(request):
#     return render(request, 'Home.html')

def Add_Locations(request):
    if backend.get_active() == True:
        return render(request, 'add_location.html')
    else:
        return redirect("Index")

def get_all_locations():
    location : list
    location = Locations.objects.values_list('loc_name', flat=True)
    # Employees.objects.values_list('eng_name', flat=True)
    return location

@api_view(['POST'])
def location_save(request):
    if backend.get_active() is True:
        loc_alias = request.POST.get("Location_alias")
        loc_address = request.POST.get("Location_address")
        loc = Locations(loc_name=loc_alias, loc_address=loc_address)
        loc.save()
        return redirect('Transport_Request')
    else:
        return redirect("Index")
    

def plan_trip(request):
    travel_from = request.POST.get("Travel_from")
    travel_to   = request.POST.get("Travel_To")
    Return_to   = request.POST.get( "Return_To" )

    if travel_from == travel_to or travel_to == Return_to:
        if 'Message' in request.session:
            del request.session['Message']

        request.session['Message'] = "'Travel From' cannot be same as 'Travel To' and 'Travel To' cannot be same as 'Return To'"
        print("MESSAGE:" + request.session['Message'])
        # return redirect('Transport_Request', context = context)
        return redirect('Transport_Request')

    Emp_id = backend.get_current_logged_in()
    distance = 10
    last_updated_price = Fuel_Prices.objects.filter(fuel_type = 'PETROL').order_by('-fuel_date').first()


    if distance > 0 and last_updated_price.fuel_price > 0:
        cost = (distance / 10)*last_updated_price.fuel_price
    else:
        cost = 0

    Trip = Trips(travel_from = travel_from, travel_to = travel_to, emp_id = Emp_id, travel_return_to = Return_to, travel_distance = distance, cost = cost, fuel = last_updated_price.fuel_price  )
    Trip.save()
    return redirect('Home')

def add_petrol_price(request):
    ft = request.POST.get("fuel_type")
    fpp = request.POST.get("fuel_price")
    fp = Fuel_Prices(fuel_price = fpp, fuel_type = ft)
    fp.save()

    return render(request, "add_petrol.html")

def history(request):
    return render(request, "history.html")