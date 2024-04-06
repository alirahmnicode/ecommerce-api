from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.shortcuts import render
from django.http.response import HttpResponse
import requests


@cache_page(5 * 60)
def cache_test(request):
    response = requests.get("https://httpbin.org/delay/2")
    data = response.json()
    return HttpResponse(data)
