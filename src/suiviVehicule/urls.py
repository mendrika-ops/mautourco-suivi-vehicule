from django.urls import path
from suiviVehicule.views import *

urlpatterns = [
    path('index/', index),
    path("article_<str:numpage>", article),
    path("register", register_request, name="signin"),
    path("", dashboard_request, name="login"),
    path("dashboard", dashboard_request),
    path("dashboard/", dashboard_request),
    path("map/<str:pos>", googlemap_request),
    path("refresh", refresh_request),
    path("onerefresh/<str:idstatusposdetail>/<str:id>", one_refresh_request),
    path("record/save", comment_request),
    path("record/listes", log_request),
    path("parameter/update/<str:id>", parameter_update_request),
    path("parameter/list", parameter_liste_request),
    path("chargement", rechange_request),
    path("api/refresh", last_api_request),
    path("planning/list", log_planning_request),
    path("log/export", export_users_xls),
    path("log/recap", recaprefresh_request),
    path("parameter/refresh", parameter_refresh)
    
]