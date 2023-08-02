import csv

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings

def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    with open(settings.BUS_STATION_CSV, encoding = 'UTF-8', newline= '') as csvf:
        reader = csv.DictReader(csvf)
        result = []
        for row in reader:
            data = {
                'Name': row['Name'],
                'Street': row['Street'],
                'District': row['District']
            }
            result.append(data)

    page_number = int(request.GET.get('page', 1))
    pagi = Paginator(result, 15)
    number = pagi.get_page(page_number)

    context = {
        'bus_stations': number,
        'page': number,
    }
    return render(request, 'stations/index.html', context)
