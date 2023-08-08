from django.shortcuts import render, HttpResponse,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Users, Locations
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
            context = {
                "message": "Login successful"
            }
            return redirect("Home")
            # return render(request, 'Home.html', context=context)
        else:
            context = {
                "message": "Login failed"
            }
            # return render(request, 'index.html', context=context)
            return redirect("Index")


def Trans_req(request):
    data = get_all_locations()
    context = {
        'Location_alias' : data
    }
    # context = [get_all_locations()]
    # print(context['Location_alias'])
    #
    # loc = context['Location_alias']
    # for locations in loc:
    #     print(locations)
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
    # Check for session persistence
    # ******************************
    # print("RETURNING", backend.get_active())
    # ******************************

    if backend.get_active() == True:
        return render(request, 'home.html')
    else:
        return redirect("Index")

def test(request):
    return render(request, 'Home.html')

def Add_Locations(request):
    if backend.get_active() == True:
        return render(request, 'add_location.html')
    else:
        return redirect("Index")

def get_all_locations():
    location : list
    location = Locations.objects.values_list('loc_name', flat=True)
    # Employees.objects.values_list('eng_name', flat=True)
    print(location)
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


