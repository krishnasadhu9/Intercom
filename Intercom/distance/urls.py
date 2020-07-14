from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [

path("",views.viewall,name="home"),
path("intercom",views.intercom_view, name="intercom")
]
