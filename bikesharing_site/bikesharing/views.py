from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse
from django.template.loader import render_to_string

def index(request):
    return render(request, 'bikesharing/index.html')

def about(request):
    return render(request, 'bikesharing/about.html')

def station_detail(request, station_id):
    return HttpResponse(f"<h1>Bike Station Details</h1><p>ID: {station_id}</p>")

def station_by_slug(request, station_slug):
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>Bike Station Details</h1><p>Slug: {station_slug}</p>")

def archive(request, year):
    if year > 2023:
        return redirect('home', permanent=True)
    return HttpResponse(f"<h1>Bike Sharing Archive</h1><p>Year: {year}</p>")

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Bike Sharing Page Not Found</h1>')