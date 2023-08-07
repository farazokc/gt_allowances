from django.shortcuts import render, HttpResponse,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Users
# from django.contrib.auth import authenticate
from allowances.auth import MyBackend

backend = MyBackend()
def index(request):
    return render(request, 'index.html')

@api_view(['POST'])
def Login(request):


    # print("Hello")
    emp_id = request.POST.get("emp_id")
    emp_pass = request.POST.get("emp_pass")

    user = Users(emp_id, emp_pass)

    session_user = backend.authenticate(request,emp_id=emp_id,emp_pass=emp_pass)

    if session_user:
        context = {
            "message": "Login successful"
        }
        return render(request, 'home.html', context=context)
    else:
        context = {
            "message": "Login failed"
        }
        # return render(request, 'index.html', context=context)
        return redirect("Index")


def Trans_req(request):
    if backend.get_active() == True:
        return render(request, 'transRequest.html')
    else:
        return redirect("Index")


def payment(request):
    if backend.get_active() == True:
        return render(request, 'allowances.html')
    else:
        return redirect("Index")


def Home(request):
    if backend.get_active() == True:
        return render(request, 'home.html')
    else:
        return redirect("Index")



