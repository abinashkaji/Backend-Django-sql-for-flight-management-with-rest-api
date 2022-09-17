from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Flight,Airport,Passenger
def index(request):
    flights=Flight.objects.all()
    return render(request,"flight/index.html",{"flights":flights})
# Create your views here.

def flight(request,fid):
    flight=Flight.objects.get(id=fid)
    passenger=flight.passengers.all() #
    non_passenger=Passenger.objects.exclude(flights=flight).all()
    return render(request,"flight/flight.html",{"flight":flight, "passengers":passenger, "non_passengers":non_passenger})

def book(request,fid):
    flight=Flight.objects.get(pk=fid)
    if request.method=="POST":
        pid=int(request.POST["Non_passenger"]) #
        passenger=Passenger.objects.get(pk=pid)
        passenger.flights.add(flight)
    return HttpResponseRedirect(reverse("flight", args=(fid,)))
    