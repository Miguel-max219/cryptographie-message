from django.contrib import admin
from django.urls import path
from chat import views
from django.http import HttpResponse
from django.views.decorators.http import require_GET

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('<str:room>/', views.room, name='room'),
    path('checkview', views.checkview, name="checkview"),
    path('send', views.send, name="send"),
    path('getMessages/<str:room>/', views.getMessages, name="getMessages"),
]

def favicon_view(request):
    return HttpResponse(status=204)

path("favicon.ico/", favicon_view),