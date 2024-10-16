from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
import pytz

def dummypage(request):
     if request.method == "GET": 
         return HttpResponse("No content here, sorry!")

def time_view(request):
    #chicago time zone
    timezone = pytz.timezone('America/Chicago')

    #get current time
    time = datetime.now(timezone)

    #format
    formatted_time = time.strftime('%H:%M')

    return HttpResponse(formatted_time)

def sum_view(request):
    num_1 = float(request.GET.get('n1', '0'))
    num_2 = float(request.GET.get('n2', '0'))

    total = num_1 + num_2

    return HttpResponse(total) 
