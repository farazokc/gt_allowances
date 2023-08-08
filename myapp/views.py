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
    print(get_all_locations())
    if backend.get_active() is True:
        return render(request, 'transRequest.html')
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


def get_all_locations():
    location : list
    location = Locations.objects.values_list('loc_id', flat=True)
    # Employees.objects.values_list('eng_name', flat=True)
    print('Hello')
    return location