from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from .models import Flight, Passenger

def index(request):
    context = {
        "flights": Flight.objects.all()
    }
    return render(request, "flights/index.html", context)

def flight(request, flight_id):
    try:
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Sorry but this flight does not exist.")
    context = {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    }
    return render(request, "flights/flight.html", context)

def book(request, flight_id):
    try:
        passenger_id = int(request.POST["passenger"])
        passenger = Passenger.objects.get(pk=passenger_id)
        flight = Flight.objects.get(pk=flight_id)
    except Passenger.DoesNotExist:
        return render(request, "flights/error.html", {"message": "No Passenger."})
    except Flight.DoesNotExist:
        return render(request, "flights/error.html", {"message": "No Flight."})
    except KeyError:
        return render(request, "flights/error.html", {"message": "No selection."})

    passenger.flights.add(flight)
    return HttpResponseRedirect(reverse("flight", args=(flight_id,)))
