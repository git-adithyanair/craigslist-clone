from django.shortcuts import render
from bs4 import BeautifulSoup

# Create your views here.

def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get("search")
    data_to_send = {"search": search}
    return render(request, 'my_app/new_search.html', data_to_send)