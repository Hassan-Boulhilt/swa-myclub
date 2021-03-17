from django.http.response import HttpResponse
from django.shortcuts import render
from datetime import date



def index(request):
    t = date.today()
    month = date.strftime(t, '%b')
    year = t.year
    title = f"MyClub Event - {month}, {year}"
    return HttpResponse(f'<h1>{title}</h1>')
