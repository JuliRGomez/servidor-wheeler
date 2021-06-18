from django.shortcuts import render
from django.http import HttpResponse
import datetime


def infoView(request,**kwargs):
    date = str(kwargs.get("month")) + '-' + str(kwargs.get("day")) + '-' + str(kwargs.get("year")) + '-' + str(        kwargs.get("h")) + '-' + str(kwargs.get("m")) + '-' + str(kwargs.get("s"))
    date1 = f'img/emg_average_{date}.png'
    date2 = f'img/boxplot_{date}.png'
    date3 = f'img/heatmap_{date}.png'
    return render(
        request,
        'index.html',
        context={'date1': date1, 'date2': date2, 'date3': date3},
    )

    """
    now = datetime.datetime.now()
    html =
    return HttpResponse(html)
    """