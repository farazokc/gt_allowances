from django.shortcuts import render, HttpResponse,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Users

# from .templates.login import empid, emp_pass
# Create your views here.
def index(request):
    return render(request, 'index.html')


@api_view(['POST'])
def Login(request):


    # print("Hello")
    emp_id = request.POST.get("emp_id")
    emp_pass = request.POST.get("emp_pass")

    user = Users(emp_id, emp_pass)

    session_user = Users.objects.filter(emp_id=emp_id,emp_pass=emp_pass)

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
    return render(request, 'transRequest.html')

def payment(request):
    return render(request, 'allowances.html')

def Home(request):
    return render(request, 'home.html')



