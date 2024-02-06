import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from news.models import (
    Headline, 
)
from news.scraper import scrape_news
from django.http import HttpResponse
from .tasks import auto_scrape_news
from django.utils import timezone
from django.http import JsonResponse
from django.views import View

"""
    This function aims at checking for updates, it check if the are records in
    the database with notification_sent=False
"""
def check_for_updates(request):
    new_updates = Headline.objects.filter(notification_sent=False).exists()
    return JsonResponse({'new_updates': new_updates})


"""
    Main view that does the scrapping, it calls a method scrape_news
"""
def scrape(request, name):
    scrape_news(name)
    return redirect("../")


"""
    This method aims at testing the task auto_scrape_news when called
    from the html the function is rendering to i.e ('news/test.html').
"""
def test_scrape_news(request):
    target_names = ['politics', 'sports', 'latest']
    updates = Headline.objects.all()[::-1]
    auto_scrape_news.delay(target_names)
    context = {
        "updates": updates
    }
    return render(request, 'news/test.html', context)


def homepage(request):
    headlines = Headline.objects.all()[::-1]
    current_time = timezone.now()
    context = {
        "object_list": headlines,
        "current_time": current_time,
    }
    return render(request, "blog/index.html", context)
   

def aboutproject(request):
    current_time = timezone.now()
    context = {
        "current_time": current_time,
    }
    return render(request, "blog/aboutproject.html", context)


def contact(request):
    return render(request, "blog/contact.html")


def basepage(request):
    headlines = Headline.objects.all()[::-1]
    context = {
        "object_list": headlines,
    }
    return render(request, "blog/base.html", context)

