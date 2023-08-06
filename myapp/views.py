from django.shortcuts import render, HttpResponse
# from .templates.login import empid, emp_pass
# Create your views here.
def index(request):
    return render(request, 'login.html')

def Signin(request):
    # if request.method == "POST":
    #     address = request.POST.get('emp_id')
    #     name = request.POST.get('emp_pass')
    print("HELLO WORLD")
    return render(request, 'Home.html') 

def Trans_req(request):
    return render(request, 'Trans_Request.html')

def payment(request):
    return render(request, 'allowances.html')






