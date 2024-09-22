import json
import xlwt
from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime
from suiviVehicule.export import Recordexport
from suiviVehicule.forms import SigninForm, LoginForm, SearchForm ,CommentFrom, ParameterForm, ParameterRefreshForm
from suiviVehicule.models import Recordcommenttrajet, TrajetcoordonneeSamm, RefreshTime
from suiviVehicule.planning import planning
from suiviVehicule.services import Services
from django.conf import settings
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from suiviVehicule.trip_service import TripService
from django.core import serializers

# Create your views here.
def index(request):
    date = datetime.today()
    title = "Suivi Trajet Vehicule"
    return render(request, "suiviVehicule/index.html", context={"title": title, "date": date})


def article(request, numpage):
    if numpage in ["01", "02", "03"]:
        return render(request, f"suiviVehicule/article_{numpage}.html")
    return render(request, "suiviVehicule/error.html")


def login_request(request):
    form = LoginForm(request.POST)
    if form.is_valid() and request.POST.get("mail") != None and request.POST.get("pswd") != None:
        if form.checkUser():
            return redirect("/dashboard")
        else:
            error = "Your idenfiant or password is wrong, please verify! "
            return render(request=request, template_name="suiviVehicule/login.html",
                          context={"login_form": form, "error": error})
    else:
        return render(request=request, template_name="suiviVehicule/login.html", context={"login_form": form})


def register_request(request):
    error = ""
    if request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():
            if form.isExist():
                error = "Email already existed,please verify!"
                return render(request, "suiviVehicule/signin.html", context={"register_form": form, "error": error})
            user = form.save()
            error = "Register successful"
            return render(request, "suiviVehicule/signin.html", context={"register_form": form, "error": error})
        else:
            return render(request, "suiviVehicule/pages/error.html")
    form = SigninForm()
    return render(request=request, template_name="suiviVehicule/signin.html", context={"register_form": form})

def setForm(request):
    if request.GET.get("reset") is None:
        return SearchForm(request.GET)
    else:
        return SearchForm()

def check(checked):
    obj = "checked"
    if checked == 'on' :
        return obj
    return ""

def dashboard_request(request):
    data_list = []
    load_value = 0
    defaut = 50
    cron_minute = RefreshTime.objects.latest("date_time").value
    service = Services()
    is_disable = False
    form = setForm(request)
    data_list = []
    
    if request.GET.get("page") is not None and request.GET.get("page").isnumeric() == True:
        data_list = service.get_data(form, int(request.GET.get("page")) ,defaut)
        load_value = int(request.GET.get("page")) +defaut
    else:
        data_list = service.get_data(form, load_value,defaut)
        load_value = len(data_list)

    data_search = service.get_new_data()
    record = CommentFrom(request.GET)
    refresh = service.get_last_refresh()
    chart = service.data_chart()
    count = service.getall_data_count(form) 
    FromPlace = request.GET.get("FromPlace")
    ToPlace = request.GET.get("ToPlace")
    statuses = request.GET.get("status")
    vehicleno = request.GET.get("vehicleno")
    if FromPlace is None:
        FromPlace =""
    if ToPlace is None:
        ToPlace =""
    if statuses is None:
        statuses =""
    if vehicleno is None:
        vehicleno =""
    legend = service.get_liste_parameter_activate()
    if load_value >= count:
        is_disable = True
        load_value = count
    elif load_value == 0:
        is_disable = True
        count = 0

    return render(request, "suiviVehicule/pages/dashboard.html",
                  context={"data_list": data_list, 
                           "data_auto": data_search, 
                           "last_refresh": refresh, 
                           "chart": json.dumps(chart), 
                           "form_search": form, 
                           "load_value": load_value, 
                           "record": record, 
                           "cron_minute": cron_minute,
                           "is_disable": is_disable,
                           "legend":legend,
                           "total_page":count,
                           "FromPlace":FromPlace,
                           "ToPlace":ToPlace,
                           "status":statuses,
                           "vehicleno":vehicleno,
                           "now": Services().date_time()})

def googlemap_request(request, pos):
    return redirect("https://www.google.com/maps?q=" + pos)


def refresh_request(request):
    try:
        Services().refresh()
    except Exception as e:
        messages.error(request, e)
    return redirect("/dashboard")

def one_refresh_request(request,idstatusposdetail,id):
    try:
        Services().set_one_refresh(idstatusposdetail,id)
    except Exception as e:
        messages.error(request,e)
    return redirect("/dashboard")

def comment_request(request):
    try:
        record = CommentFrom(request.GET)
        if record.is_valid():
            record.save()
    except Exception as e:
        messages.error(request, e)
    return redirect("/dashboard")

def log_request(request):
    records = []
    datefrom = request.GET.get('datefrom')
    dateto = request.GET.get('dateto')
    try:
        records = Services().get_listes_record(datefrom ,dateto)
       
    except Exception as e:
        messages.error(request, e)
    return render(request, "suiviVehicule/pages/log_record.html",context={"data_list": records, "datefrom": datefrom, "dateto":dateto})

def parameter_update_request(request,id):
    param = ParameterForm(request.POST)  
    try:
        parameter = Services().get_liste_parameter_byId(id)
        if request.method == 'POST': 
            param = ParameterForm(request.POST)
            if param.is_valid() :
                param.update(parameter)
                parameter = Services().get_liste_parameter_byId(id)
                return redirect("/parameter/list")
        param = ParameterForm(instance=parameter) 
    except Exception as e:
        messages.error(request, e)
    return render(request, "suiviVehicule/pages/update_parameter.html",context={"form": param})

def parameter_liste_request(request):
    data = Services().get_liste_parameter()
    return render(request, "suiviVehicule/pages/liste_parameter.html",context={"data_list": data})

def rechange_request(request):
    Services().rechange()
    return render(request, "suiviVehicule/pages/error.html", context={"error": "Notify: loading data"})

def last_api_request(request):
    refresh = Services().get_last_refresh()
    now = Services().date_time()
    print("Api refresh - ", refresh)
    return JsonResponse({'now': now, 'datetime': refresh, 'result': '200'})

def log_planning_request(request):
    defaut = str(Services().date_time().strftime('%Y-%m-%d'))
    datefrom = defaut
    dateto = defaut
    if request.GET.get('datefrom') is not None and request.GET.get('dateto') is not None:
        datefrom = request.GET.get('datefrom')
        dateto = request.GET.get('dateto') 
               
    data = planning().get_list_planning(datefrom, dateto)
    return render(request, "suiviVehicule/pages/log_planning.html",context={"data_list": data})



def export_users_xls(request):
    Services().date_time()
    datefrom = request.GET.get('datefrom')
    dateto = request.GET.get('dateto')
    dateinfrom = datetime. strptime(datefrom, '%Y-%m-%d')
    dateinto = datetime. strptime(dateto, '%Y-%m-%d')
    filename = "log_data_"+ datefrom +"_"+dateto+".xls" 
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename='+filename

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Driver name', 'Driveer Mob No','Vehicule No', 'Trip ID' ,  'Pickup Place', 'Destination' ,'Current postion', 'Pick up time', 'Date' , 'Actual Time', 'Difference' , 'Comments', 'Status']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = Recordexport.objects.filter(daterecord__range = [dateinfrom,dateinto]).values_list( 'driver_oname', 'driver_mobile_number','vehicleno', 'id_trip', 'FromPlace','ToPlace', 'current' , 'pick_up_time', 'daterecord','actualtime', 'difftimepickup', 'comment', 'status').order_by('daterecord','actualtime')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def recaprefresh_request(request):
    data = []
    datefrom = None
    dateto = None
    if request.GET.get('datefrom') is not None and request.GET.get('dateto') is not None:
        datefrom = request.GET.get('datefrom')
        dateto = request.GET.get('dateto') 
    
    data = Services().getRecaprefresh(datefrom, dateto)
    return render(request, "suiviVehicule/pages/log_recap.html",context={"data_list": data, "sum_api": sum(data.values_list('nbre_call_api', flat=True)) })

def parameter_refresh(request):
    param = ParameterRefreshForm(request.GET)  
    try:
        parameter = RefreshTime.objects.latest("date_time")
        if request.method == 'GET': 
            if param.is_valid() :
                param.save()
                parameter = RefreshTime.objects.latest("date_time")
                return redirect("/parameter/refresh")
        param = ParameterRefreshForm(instance=parameter) 
    except Exception as e:
        messages.error(request, e)
    return render(request, "suiviVehicule/pages/refresh_parameter.html", context={"form": param})

def trip_detail_request(request, id_trip):
    data = Services().get_data_by_idtrip(id_trip)
    return render(request, "suiviVehicule/pages/trip_detail.html", context={"item": data})

def trip_cancel_request(request, id_trip):
    trip = TripService()
    service = Services()
    data = service.get_data_by_idtrip(id_trip)

    # Récupérer les motifs et sous-motifs
    reasons = trip.get_reason_list()
    subreasons_queryset = trip.get_subreason_list()

    # Convertir les sous-motifs en format JSON
    subreasons = list(subreasons_queryset.values("id", "sub_reason_name", "reason"))
    subreasons_json = json.dumps(subreasons)

    return render(request, "suiviVehicule/pages/trip_canceling.html", context={
        "item": data,
        "reasons": reasons,
        "subreasons": subreasons_json
    })


def trip_cancel_action(request, id_trip):
    trip = TripService()
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            reason_id = data.get('reason_id')
            sub_reason_ids = data.get('sub_reason_ids')
            print("Reason ", reason_id, " Sub reason ", sub_reason_ids)

            #Record comment
            record = trip.save_record_comment(id_trip, "My record")
            trip.save_reason_record(record, reason_id)
            trip.save_subreason_record(record, sub_reason_ids)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
        
def trip_get_current_reason(request, id_trip):
    trip = TripService()
    current_reasons_queryset = trip.get_subreason_recorded_current(id_trip)
    current_reasons =  list(current_reasons_queryset.values())
    # current_reasons_json = json.dumps(current_reasons)
    # print("current : " + current_reasons)  
    return JsonResponse(current_reasons, safe=False)

def trip_remove_reason(request, id_trip):
    trip = TripService()
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            reason_id = data.get('reason_id')
            sub_reason_ids = data.get('sub_reason_ids')
            subs = trip.sub_record_json_to_object(sub_reason_ids)
            trip.change_state_reason_record(id_trip, reason_id, subs, 0)
            return JsonResponse({'success': True}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

def trip_remove_sub_reason(request, id_trip):
    return JsonResponse({'success': False}, status=400)




