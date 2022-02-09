
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import include, path

def indexRedirect(req):
    return HttpResponseRedirect("tasks/")


urlpatterns = [
    path("admin/", admin.site.urls),
    path('user/' , include("user.urls")),
    path('tasks/' , include("tasks.urls")),
    path('' , indexRedirect)

]

