from django.urls import path
from suiviVehicule.views import index, article, register_request, login_request, dashboard_request, googlemap_request, \
    refresh_request, one_refresh_request, comment_request, log_request

urlpatterns = [
    path('index/', index),
    path("article_<str:numpage>", article),
    path("register", register_request, name="signin"),
    path("", login_request, name="login"),
    path("dashboard", dashboard_request),
    path("map/<str:pos>", googlemap_request),
    path("refresh", refresh_request),
    path("onerefresh/<str:idstatusposdetail>/<str:id>", one_refresh_request),
    path("record/save", comment_request),
    path("record/listes", log_request),
]