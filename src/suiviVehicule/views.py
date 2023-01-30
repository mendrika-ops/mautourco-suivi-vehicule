from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime

from suiviVehicule.forms import SigninForm, LoginForm, dashboardForm
from suiviVehicule.services import services


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
    if form.is_valid():
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


def dashboard_request(request):
    form = dashboardForm()
    data_list = services().get_data()
    refresh =  services().get_last_refresh()
    print("last refresh ", refresh)
    return render(request, "suiviVehicule/dashboard.html", context={"data_list": data_list, "last_refresh": refresh})


def googlemap_request(request, pos):
    serv = services()
    #map = serv.get_direction()
    #print("indro mapp ", map)

    data_list = services().get_data()
    #return render(request, "suiviVehicule/dashboard.html", context={"data_list": data_list})
    return redirect("https://www.google.com/maps?q=" + pos)


def refresh_request(request):
    status = services().gestion_status_pos()
    return redirect("/dashboard")