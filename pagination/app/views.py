from django.shortcuts import render_to_response, redirect
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Paginator
import csv


def index(request):
    return redirect(reverse(bus_stations))

# [{'Name': 'название', 'Street': 'улица', 'District': 'район'}]
def bus_stations(request):
    current_page = int(request.GET.get('page',1))
    next_page_url = '?page=' + str(current_page + 1)
    page_len = 15
    with open(settings.BUS_STATION_CSV, mode='r', encoding='cp1251') as infile:
        csvdata = list(csv.DictReader(infile, delimiter=','))

    paginator = Paginator(csvdata, page_len)
    page = paginator.get_page(current_page)
    print(page.has_next())
    print(page.has_previous())
    return render_to_response('index.html', context={
        'bus_stations': page,
        'current_page': current_page,
        'prev_page_url': None,
        'next_page_url': next_page_url,
        })

    '''
    n = len(csvdata)
    pages_num = int(n / page_len)
    if pages_num <= 0 :
        pages_num= 1
    if current_page > pages_num:
        current_page = pages_num
    data_on_page = csvdata[(current_page - 1 ) * page_len : current_page * page_len]
    mydata = [{'Name':'«Бескудниково», Дмитровское шоссе (от центра)','Street':'Дмитровское шоссе','District':'Северный административный округ,Бескудниковский район'},{'Name':'«Бескудниково», Дмитровское шоссе (от центра)','Street':'Дмитровское шоссе','District':'Северный административный округ,Бескудниковский район'}]
    return render_to_response('index.html', context={
        'bus_stations': data_on_page,
        'current_page': current_page,
        'prev_page_url': None,
        'next_page_url': next_page_url,
        })
    '''

