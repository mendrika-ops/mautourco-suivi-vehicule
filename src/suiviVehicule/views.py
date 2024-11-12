import json
from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from datetime import datetime
from suiviVehicule.forms import SigninForm, LoginForm, SearchForm, CommentFrom, ParameterForm, ParameterRefreshForm
from suiviVehicule.models import *
from suiviVehicule.planning import planning
from suiviVehicule.service.services import Services
from django.conf import settings
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from suiviVehicule.service.trip_service import TripService
from django.core import serializers
from suiviVehicule.export import Export
from dateutil.relativedelta import relativedelta
from suiviVehicule.service.ia_service import IAService
from django.contrib.auth.decorators import login_required
from decimal import Decimal
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
    if checked == 'on':
        return obj
    return ""

def load_login(request):
    return redirect('/user/login')

def load_init(request):
    return redirect('/user/init')

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
        data_list = service.get_data(
            form, int(request.GET.get("page")), defaut)
        load_value = int(request.GET.get("page")) + defaut
    else:
        data_list = service.get_data(form, load_value, defaut)
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
        FromPlace = ""
    if ToPlace is None:
        ToPlace = ""
    if statuses is None:
        statuses = ""
    if vehicleno is None:
        vehicleno = ""
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
                           "legend": legend,
                           "total_page": count,
                           "FromPlace": FromPlace,
                           "ToPlace": ToPlace,
                           "status": statuses,
                           "vehicleno": vehicleno,
                           "now": Services().date_time()})

@login_required
def googlemap_request(request, pos):
    return redirect("https://www.google.com/maps?q=" + pos)

@login_required
def refresh_request(request):
    try:
        if not request.user.is_superuser:
            return redirect('/user/noaccess')
        Services().refresh()
    except Exception as e:
        messages.error(request, e)
    return redirect("/dashboard")


def one_refresh_request(request, idstatusposdetail, id):
    try:
        Services().set_one_refresh(idstatusposdetail, id)
    except Exception as e:
        messages.error(request, e)
    return redirect("/dashboard")

@login_required
def comment_request(request):
    try:
        record = CommentFrom(request.GET)
        if record.is_valid():
            record.save()
    except Exception as e:
        messages.error(request, e)
    return redirect("/dashboard")

@login_required
def log_request(request):
    records = []
    service = Services()
    legend = service.get_liste_parameter_activate()
    datefrom = request.GET.get('datefrom')
    dateto = request.GET.get('dateto')
    status = request.GET.get('status')
    try:
        if not datefrom:
            datefrom = datetime.now().strftime('%Y-%m-%d')
        if not dateto:
            dateto = datetime.now().strftime('%Y-%m-%d')
        records = service.get_listes_record(datefrom, dateto, status)

    except Exception as e:
        messages.error(request, e)
    return render(request, "suiviVehicule/pages/log_record.html", 
                  context={
                      "data_list": records, 
                      "datefrom": datefrom, 
                      "dateto": dateto,
                      "legend": legend,
                      "status": status
                      })

@login_required
def parameter_update_request(request, id):
    if not request.user.is_superuser:
        return redirect('/user/noaccess')
    param = ParameterForm(request.POST)
    try:
        parameter = Services().get_liste_parameter_byId(id)
        if request.method == 'POST':
            param = ParameterForm(request.POST)
            if param.is_valid():
                param.update(parameter)
                parameter = Services().get_liste_parameter_byId(id)
                return redirect("/parameter/list")
        param = ParameterForm(instance=parameter)
    except Exception as e:
        messages.error(request, e)
    return render(request, "suiviVehicule/pages/update_parameter.html", context={"form": param})

@login_required
def parameter_liste_request(request):
    if not request.user.is_superuser:
        return redirect('/user/noaccess')
    data = Services().get_liste_parameter()
    return render(request, "suiviVehicule/pages/liste_parameter.html", context={"data_list": data})


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
    return render(request, "suiviVehicule/pages/log_planning.html", context={"data_list": data})

@login_required
def export_users_xls(request):
    Services().date_time()
    datefrom = request.GET.get('datefrom')
    dateto = request.GET.get('dateto')
    response = Export().export_record(datefrom, dateto)
    return response

@login_required
def recaprefresh_request(request):
    if not request.user.is_superuser:
        return redirect('/user/noaccess')
    
    datefrom = request.GET.get('datefrom')
    dateto = request.GET.get('dateto')
    if not datefrom:
        datefrom = (datetime.now() - relativedelta(months=1)).strftime('%Y-%m-%d')
    if not dateto:
        dateto = datetime.now().strftime('%Y-%m-%d')

    data = Services().getRecaprefresh(datefrom, dateto)
    return render(request, "suiviVehicule/pages/log_recap.html", context={"data_list": data, "sum_api": sum(data.values_list('nbre_call_api', flat=True))})

@login_required
def parameter_refresh(request):
    if not request.user.is_superuser:
            return redirect('/user/noaccess')
    
    param = ParameterRefreshForm(request.GET)
    try:
        parameter = RefreshTime.objects.latest("date_time")
        if request.method == 'GET':
            if param.is_valid():
                param.save()
                parameter = RefreshTime.objects.latest("date_time")
                return redirect("/parameter/refresh")
        param = ParameterRefreshForm(instance=parameter)
    except Exception as e:
        messages.error(request, e)
    return render(request, "suiviVehicule/pages/refresh_parameter.html", context={"form": param})

@login_required
def trip_detail_request(request, id_trip):
    iaService = IAService()
    data = Services().get_data_by_idtrip(id_trip)
    details = Services().get_detail_info(id_trip)
    dates = [entry.daty_time.strftime('%H:%M:%S') for entry in details]
    speeds = [entry.speed for entry in details]
    return render(request, "suiviVehicule/pages/trip_detail.html", 
                  context={"item": data, 
                            "details": details,
                            "dates": dates,
                            "speeds": speeds})

@login_required
def trip_prediction_request(request, id_trip):
    iaService = IAService()
    data = Services().get_data_by_idtrip(id_trip)
    details = Services().get_detail_info(id_trip)
    dates = [entry.daty_time.strftime('%H:%M:%S') for entry in details]
    anormaly = [entry.annulated for entry in details]
    risky = [entry.risky for entry in details]
    completed = [entry.completed for entry in details]
    
    return render(request, "suiviVehicule/pages/trip_prediction.html", 
                  context={"item": data,
                           "dates": dates,
                           "details": details,
                           "anormaly": anormaly,
                           "risky": risky,
                           "completed": completed})

@login_required
def trip_cancel_request(request, id_trip):
    trip = TripService()
    service = Services()
    data = service.get_data_by_idtrip(id_trip)

    # Récupérer les motifs et sous-motifs
    reasons = trip.get_reason_list()
    subreasons_queryset = trip.get_subreason_list()

    # Convertir les sous-motifs en format JSON
    subreasons = list(subreasons_queryset.values(
        "id", "sub_reason_name", "reason"))
    subreasons_json = json.dumps(subreasons)

    record = trip.get_record_comment(id_trip)

    return render(request, "suiviVehicule/pages/trip_canceling.html", context={
        "item": data,
        "reasons": reasons,
        "subreasons": subreasons_json,
        "current_date": record.datetime.strftime('%Y-%m-%dT%H:%M') if record is not None else '',
        "comment" : record.comment if record is not None else ''
    })

@login_required
def trip_cancel_action(request, id_trip):
    trip = TripService()
    if request.method == 'POST':  
        try:
            data = json.loads(request.body)
            reason_id = data.get('reason_id')
            sub_reason_ids = data.get('sub_reason_ids')

            record = trip.get_record_comment(id_trip)
            # Record comment
            trip.save_reason_record(record, reason_id)
            trip.save_subreason_record(record, sub_reason_ids)
            return JsonResponse({'success': True})
        except Exception as e:
            messages.error(request, e)

@login_required
def trip_cancel_action_savecomment(request, id_trip):
    trip = TripService()
    if request.method == 'POST':
        try:
            comment = request.POST.get("comment")
            date = request.POST.get("date")
            print("les 2 " , comment, date)
            record = trip.save_record_comment(id_trip, comment, date)
        except Exception as e:
            messages.error(request, e)
    return redirect("/trip/cancel/"+ id_trip)

@login_required
def trip_get_current_reason(request, id_trip):
    trip = TripService()
    current_reasons_queryset = trip.get_subreason_recorded_current(id_trip)
    current_reasons = list(current_reasons_queryset.values())
    # current_reasons_json = json.dumps(current_reasons)
    # print("current : " + current_reasons)
    return JsonResponse(current_reasons, safe=False)

@login_required
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

@login_required
def trip_remove_sub_reason(request, id_trip):
    return JsonResponse({'success': False}, status=400)

@login_required
def update_record_data_api(request):
    # try:
    # Services().update_vehicule_parameter_record()
    # count = 0

    # # while count != 10:
    # TripService().update_record_random()
    # count+=1
    # except Exception as e:
    #     return JsonResponse({'success': False, 'error': str(e)}, status=400)

    #iaService.loadModeleSupervisé()
    return JsonResponse({'success': True}, status=200)

@login_required
def load_visualisation(request):
    stats = VehicleFleetStatistics.objects.all().first()
    planning_week = PlanningWeekMoy.objects.filter().order_by('week')
    planning_driver_month = PlanningDriverMonth.objects.all()

    labels = [f"Week {p.week}" for p in planning_week]
    data = [float(p.average_plannings_per_day) for p in planning_week]

    return render(request, "suiviVehicule/pages/visualisation.html",
                  context={"stats" : stats,
                           'labels': json.dumps(labels),
                            'data': json.dumps(data), 
                            'planning_driver' : planning_driver_month      
                    })

@login_required
def load_kpi(request):
    service = Services()
    datefrom = request.GET.get('datefrom')
    dateto = request.GET.get('dateto')
    now = Services().date_time()
    today = now.strftime('%Y-%m-%d')
    if not datefrom:
        datefrom = (now - relativedelta(months=1))
    if not dateto:
        dateto = today

    trajetPerf = service.get_trajet_performance_summary(datefrom, dateto)

    queryset = TrajetPerformanceSummary.objects.filter(
        trip_day__range=[datefrom, dateto]
    ).order_by('trip_day')

    dates = [entry.trip_day.strftime('%Y-%m-%d') for entry in queryset]
    total_trips = [entry.total_trips for entry in queryset]
    completed_trips = [entry.completed_trips for entry in queryset]
    late_trips = [entry.late_trips for entry in queryset]
    canceled_trips = [entry.canceled_trips for entry in queryset]

    context = {
        'trajetPerf' : trajetPerf,
        'dates': dates,
        'total_trips': total_trips,
        'completed_trips': completed_trips,
        'late_trips': late_trips,
        'canceled_trips': canceled_trips,
        'datefrom': datefrom,
        'dateto': dateto,
    }
    return render(request, "suiviVehicule/pages/performance_indicator.html",
                  context)

@login_required
def load_usage_google(request):
    service = Services()
    datefrom = request.GET.get('datefrom')
    dateto = request.GET.get('dateto')
    if not datefrom:
        datefrom = (Services().date_time() - relativedelta(months=1)).strftime('%Y-%m-%d')
    if not dateto:
        dateto = Services().date_time().strftime('%Y-%m-%d')
    
    data = Services().getRecaprefresh(datefrom, dateto)

    context = {
        'data_list' : data,
        'datefrom': datefrom,
        'dateto': dateto,
        "sum_api": sum(data.values_list('nbre_call_api', flat=True))

    }
    return render(request, "suiviVehicule/pages/usage_google.html",
                  context)

