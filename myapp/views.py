# from django.contrib.auth import authenticate
from allowances.auth import MyBackend
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from datetime import date, datetime
from django.db.models import Sum
import requests
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import calendar
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .models import Users, Locations, Trips, Fuel_Prices, Reciepts



backend = MyBackend.getInstance()


def index(request):
    request.session['title'] = "Login"
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
        request.session['title'] = "Login"
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
            return redirect("Home")
        else:
            msg = backend.get_error_msg()['login_failed']
            request.session['msg'] = msg
            print("LOGIN FAIL MESSAGE: ", request.session['msg'])
            return   redirect("Index")


                # return render(request, 'index.html', context=context)



@api_view(['POST'])
def Logout(request):
    backend.logout()
    return redirect("Index")

# {
#     "destination_addresses": [
#         "Gatronova House, 10 Beaumont Rd, Civil Lines Karachi, Karachi City, Sindh, Pakistan"
#     ],
#     "origin_addresses": [
#         "Drigh Rd Station Rd, Drigh Road Drigh Colony Shah Faisal Colony, Karachi, Karachi City, Sindh, Pakistan"
#     ],
#     "rows": [
#         {
#             "elements": [
#                 {
#                     "distance": {
#                         "text": "12.7 km",
#                         "value": 12749
#                     },
#                     "duration": {
#                         "text": "20 mins",
#                         "value": 1209
#                     },
#                     "origin": "Drigh Road Station Road, Drigh Road Drigh Colony Shah Faisal Colony, Karachi",
#                     "destination": "Gatronova House, Beaumont Road, Civil Lines Karachi",
#                     "status": "OK"
#                 }
#             ]
#         }
#     ],
#     "status": "OK"
# }


def Trans_req(request):
    if backend.get_active() is True:

        request.session['title'] = "Transport Request"
        data = get_all_locations()
        LOV = {
            'Location_alias': data,
        }
        if request.method == 'POST':
            travel_from_alias = request.POST.get("Travel_from")
            travel_to_alias = request.POST.get("Travel_To")
            return_to_alias = request.POST.get("Return_To")

            if travel_from_alias == travel_to_alias or travel_to_alias == return_to_alias and ( not travel_from_alias  and not travel_to_alias):
                LOV.update({'msg': backend.get_error_msg()['Trans_Req']})

            else:
                Emp_id = backend.get_current_logged_in()

                travel_from = Locations.objects.filter(loc_name=travel_from_alias, emp_id = backend.get_current_logged_in())\
                    .values('loc_address').first()
                travel_to = Locations.objects.filter(loc_name=travel_to_alias, emp_id=backend.get_current_logged_in()) \
                    .values('loc_address').first()
                return_to = Locations.objects.filter(loc_name=return_to_alias, emp_id=backend.get_current_logged_in()) \
                    .values('loc_address').first()

                # ************ DISTANCE MATRIX API ************
                key = 'LAXzSKbQ6f1w3fGeQxQN8lKM4VVqh'

                r1 = requests.get(f'https://api.distancematrix.ai/maps/api/distancematrix/json?origins={travel_from}&destinations={travel_to}&key={key}').json()
                r2 = requests.get(f'https://api.distancematrix.ai/maps/api/distancematrix/json?origins={travel_to}&destinations={return_to}&key={key}').json()
                d1 = float(r1['rows'][0]['elements'][0]['distance']['value'])
                d2 = float(r2['rows'][0]['elements'][0]['distance']['value'])
                print("d1: ", d1, "   type: ", type(d1))
                print("d2: ", d2, "   type: ", type(d2))
                distance = (d1+d2)/1000
                print("distance: ", distance, "   type: ", type(distance))

                # **********************************************

                last_updated_price = Fuel_Prices.objects.filter(fuel_type='PETROL').order_by('-fuel_date').first()

                if distance > 0 and last_updated_price.fuel_price > 0:
                    cost = (distance / 10) * last_updated_price.fuel_price
                    print("Cost: ", cost)
                else:
                    cost = 0

                Trip = Trips(travel_from=travel_from_alias, travel_to=travel_to_alias, emp_id=Emp_id, travel_return_to=return_to_alias,
                             travel_distance=distance, cost=cost, fuel=last_updated_price.fuel_price, approved = False)
                Trip.save()
                User = Users.objects.filter(emp_id = backend.get_current_logged_in()).values('Account_balance').first()
                current_balance = User['Account_balance']

                if current_balance == None:
                    current_balance = 0

                Acc_balance = current_balance + cost
                User.update(Account_balance = Acc_balance)

                LOV.update({'msg': backend.get_success()['Trans_Req']})
                print("hello Mssg: ",LOV)

            return render(request, 'transRequest.html', context = LOV)
        else:
            print("hello Mssg: ", LOV)
            return render(request, 'transRequest.html', context = LOV)
    else:
        return redirect("Index")


# def payment(request):
#     if backend.get_active() == True:
#         request.session['title'] = "Allowances"
#         print(request.session)
#         return render(request, 'allowances.html')
#     else:
#         return redirect("Index")


def Home(request):

    # print("OUTSIDE ACTIVE ACCOUNT: ", request.POST.get('travel_id'))
    if backend.get_active() == True:
        request.session['title'] = "Home"
        Trip = Trips.objects.filter( emp_id = backend.get_current_logged_in(), approved = False )
        Account_balance = Trip.aggregate(Sum('cost'))
        print("Account Balance is: ",Account_balance['cost__sum'])
        # print("INSIDE ACTIVE ACCOUNT: ",request.POST.get('travel_id'))
        travel_id = None
        travel_id = request.POST.get('travel_id')
        # print("Travel ID: ", travel_id)
        if travel_id:
            # print('true')
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

        # print("Trips: ", trip)
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
        request.session['title'] = "Add Location"
        return render(request, 'add_location.html')
    else:
        return redirect("Index")


def get_all_locations():
    location: list
    location = Locations.objects.filter(emp_id  = backend.get_current_logged_in())
    loc = location.values_list('loc_name', flat=True)
    print("LOCATIONS FROM SERVER: \n", location)
    # Employees.objects.values_list('eng_name', flat=True)
    return loc


@api_view(['POST'])
def location_save(request):

    if backend.get_active() is True:
        request.session['title'] = "Save Location"
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




def add_petrol_price(request):
    if backend.get_active() is True:
        request.session['title'] = "Fuel Prices"
        if request.method == "POST":
            request.session['title'] = "Fuel Prices"
            ft = request.POST.get("fuel_type")
            fpp = request.POST.get("fuel_price")
            fp = Fuel_Prices(fuel_price=fpp, fuel_type=ft)
            fp.save()
            return redirect("Transport_Request")
        else:
            return render(request, "add_petrol.html")
    else:
        return redirect("Index")

def allowances(request):
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    if backend.get_active() is None:
        return redirect("Index")
    global context
    context = {
        'Emp_id':None ,
        'month': None,
        'year': None,
        'Sum_Distance':None,
        'Sum_Cost': None,
        'Count': None,
        'cashed_on': None,
        'receipt_id': None,
    }
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    if request.method == 'GET': #page load
        currentMonth = datetime.now().month
        currentYear = datetime.now().year
        if request.GET.get('month'):
            currentMonth = request.GET.get('month')
            currentYear = request.GET.get('year')
            if currentMonth == '0':
                currentMonth = datetime.now().month
        request.session['title'] = "Allowances"

        Trip = Trips.objects.filter(travel_date__month= currentMonth,
                                    travel_date__year = currentYear,
                                    emp_id = backend.get_current_logged_in(),
                                    approved = False )
        Sum_Distance = Trip.aggregate(Sum('travel_distance'))
        count = Trip.count()
        Sum_Cost = Trip.aggregate(Sum('cost'))

        if Sum_Distance ['travel_distance__sum'] == None:
            Sum_Distance['travel_distance__sum'] = 0
        if count == None:
            count = 0
        if  Sum_Cost ['cost__sum'] == None:
            Sum_Cost['cost__sum'] = 0


        if currentMonth == '0':
            currentMonth = datetime.now().month
            month = calendar.month_name[int(currentMonth)]
        else:
            month = calendar.month_name[int(currentMonth)]
        context = {
            'Emp_id' : backend.get_current_logged_in(),
            'month':month,
            'year': currentYear,
            'Sum_Distance' : round(Sum_Distance ['travel_distance__sum']),
            'Sum_Cost' : round(Sum_Cost ['cost__sum']),
            'Count'     : count,
            'cashed_on': None,
            'receipt_id': None,
        }
        # Rec = Reciepts.objects.create(sum_distance = Sum_Distance['travel_distance__sum'],Total_Cost  = Sum_Cost['cost__sum'],
        #                               No_of_Trips = count, emp_id =
        #                               backend.get_current_logged_in(),dated = datetime.now())

        print(context)
        return render(request, "allowances.html", context = context)

    elif request.method == 'POST':
        Trip = Trips.objects.filter(travel_date__month__gte = currentMonth,
                                    travel_date__year__gte = currentYear,
                                    emp_id = backend.get_current_logged_in(),
                                    approved = False )
        Sum_Distance = Trip.aggregate(Sum('travel_distance'))
        count = Trip.count()
        Sum_Cost = Trip.aggregate(Sum('cost'))
        travel_id_list = []
        for Tr in Trip:
            travel_id_list.append(Tr.travel_id)
        print(    travel_id_list)
        print('Helloooo Worlddd')
        Recep = Reciepts.objects.filter(trips__travel_id__in  = travel_id_list,trips__emp_id = backend.get_current_logged_in()).values('paid', 'reciept_id','dated').distinct()
        print(Recep)
        # if Recep:
        #     if Recep.first()['paid'] == True:
        #         context = {
        #             'Emp_id': backend.get_current_logged_in(),
        #             'month': calendar.month_name[currentMonth],
        #             'year': currentYear,
        #             'Sum_Distance': round(Sum_Distance['travel_distance__sum']),
        #             'Sum_Cost': round(Sum_Cost['cost__sum']),
        #             'Count': count,
        #             'cashed_on': Recep['dated'],
        #             'receipt_id': Recep['reciept_id'],
        #             'status':'Paid',
        #         }
        #         return render(request, "allowances.html", context=context)
        print(Recep)
        if not Recep:
            Rec = Reciepts.objects.create(sum_distance=Sum_Distance['travel_distance__sum'],
                                  Total_Cost=Sum_Cost['cost__sum'],
                                  No_of_Trips=count, emp_id=
                                  backend.get_current_logged_in())
            for Tr in Trip:
                Rec.trips.add(Tr)
                Rec.save()
                context = {
                    'Emp_id': backend.get_current_logged_in(),
                    'month': calendar.month_name[currentMonth],
                    'year': currentYear,
                    'Sum_Distance': round(Sum_Distance['travel_distance__sum']),
                    'Sum_Cost': round(Sum_Cost['cost__sum']),
                    'Count': count,
                    'cashed_on': None,
                    'receipt_id': Rec.reciept_id
                }

        else:
            context = {
                'Emp_id': backend.get_current_logged_in(),
                'month': calendar.month_name[currentMonth],
                'year': currentYear,
                'Sum_Distance': round(Sum_Distance['travel_distance__sum']),
                'Sum_Cost': round(Sum_Cost['cost__sum']),
                'Count': count,
                'cashed_on': None,
                'receipt_id': Recep['reciept_id']
            }
        print(context)
        return render_to_pdf('pdf.html', context)
        return render(request, "allowances.html", context=context)

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if pdf.err:
        return HttpResponse("Invalid PDF", status_code=400, content_type='text/plain')
    return HttpResponse(result.getvalue(), content_type='application/pdf')

# api_view("POST")
# def cash_dept(request):
#     if request.method == 'POST':
#         Rec_number=request.POST.get('reciept_id')
#         Reciept = Reciepts.objects.filter(reciept_id = Rec_number, paid=False)
#         Trip_id = Reciept.values('trips__travel_id').distinct()
#         for id in Trip_id:
#             Trip = Trips.filter(travel_id = id)
#             Trip.update(approved=True)
#         if Reciept:
#             Reciept.update(paid = True, Dated=datetime.now())
#             return "The Cashed is handeled"
#         else:
#             return 'No reciept Found'


# Chat GFT code
@csrf_exempt
def cash_dept(request):
    if request.method == 'POST':
            data = json.loads(request.body)
            reciept_id = data.get('reciept_id')

            if reciept_id is not None:
                receipt = Reciepts.objects.filter(reciept_id=reciept_id, paid=False)

                if receipt.exists():
                    receipt.update(paid=True, dated=datetime.now())
                    Trip_id = Reciepts.objects.filter(reciept_id = reciept_id).values('trips__travel_id')
                    for id in Trip_id:
                        Trip = Trips.objects.filter(travel_id=id['trips__travel_id'])
                        Trip.update(approved=True)
                    return JsonResponse({"message": "Receipt has been handled"})
                else:
                    return JsonResponse({"message": "No receipt found"}, status=404)
            else:
                return JsonResponse({"message": "Invalid request data"}, status=400)
    else:
        return JsonResponse({"message": "Invalid request method"}, status=405)
