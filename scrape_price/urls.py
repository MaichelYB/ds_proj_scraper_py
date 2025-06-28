from django.urls import path
from django.http import HttpResponse

def health_check(request):
    return HttpResponse("Server is running", status=200)

urlpatterns = [
    path('health/', health_check, name='health-check'),
]
