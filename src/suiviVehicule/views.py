from django.contrib import messages
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime
import json
from suiviVehicule.forms import SigninForm, LoginForm, SearchForm ,CommentFrom, ParameterForm
from suiviVehicule.models import TrajetcoordonneeSamm
from suiviVehicule.services import services
from django.conf import settings

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
            return render(request, "suiviVehicule/error.html")
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
    service = services()
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

    return render(request, "suiviVehicule/dashboard.html",
                  context={"data_list": data_list, 
                           "data_auto": data_search, 
                           "last_refresh": refresh, 
                           "chart": json.dumps(chart), 
                           "form_search": form, 
                           "load_value": load_value, 
                           "record": record, 
                           "cron_minute":settings.JOB_MINUTE,
                           "is_disable": is_disable,
                           "legend":legend,
                           "total_page":count,
                           "FromPlace":FromPlace,
                           "ToPlace":ToPlace,
                           "status":statuses,
                           "vehicleno":vehicleno,
                           "now": services().date_time()})

def googlemap_request(request, pos):
    return redirect("https://www.google.com/maps?q=" + pos)


def refresh_request(request):
    try:
        services().rechange()
        services().gestion_status_pos()
    except Exception as e:
        messages.error(request, e)
    return redirect("/dashboard")

def one_refresh_request(request,idstatusposdetail,id):
    try:
        services().set_one_refresh(idstatusposdetail,id)
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
        records = services().get_listes_record(datefrom ,dateto)
       
    except Exception as e:
        messages.error(request, e)
    return render(request, "suiviVehicule/logrecord.html",context={"data_list": records})

def parameter_update_request(request,id):
    param = ParameterForm(request.POST)  
    try:
        parameter = services().get_liste_parameter_byId(id)
        if request.method == 'POST': 
            param = ParameterForm(request.POST)
            if param.is_valid() :
                param.update(parameter)
                parameter = services().get_liste_parameter_byId(id)
                return redirect("/parameter/list")
        param = ParameterForm(instance=parameter) 
    except Exception as e:
        messages.error(request, e)
    return render(request, "suiviVehicule/update-parameter.html",context={"form": param})

def parameter_liste_request(request):
    data = services().get_liste_parameter()
    return render(request, "suiviVehicule/liste-parameter.html",context={"data_list": data})

def rechange_request(request):
    services().rechange()
    return render(request, "suiviVehicule/error.html", context={"error": "Notify: loading data"})

def last_api_request(request):
    refresh = services().get_last_refresh()
    print("Api refresh - ", refresh)
    return JsonResponse({'datetime': refresh, 'result': '200'})