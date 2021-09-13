from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models

# Create your views here.

BASE_CRAIGSLIST_URL = "https://losangeles.craigslist.org/d/for-sale/search/sss?query={}"
BASE_CRAIGSLIST_IMAGE_URL = "https://images.craigslist.org/{}_300x300.jpg"

def home(request):
    return render(request, 'base.html')

def new_search(request):
    
    # Get search query and create new Search object.
    search = request.POST.get("search")
    models.Search.objects.create(search=search)
    
    # Build Craigslist url to scrape.
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    
    # Make request to retrieve html for webpage to scrape.
    response = requests.get(final_url)
    
    # Scrape webpage.
    soup = BeautifulSoup(response.text, features="html.parser")
    post_listings = soup.find_all("li", {"class": "result-row"})
    
    print(post_listings[0])
    
    final_postings = []
    for post in post_listings:
        title = post.find(class_="result-title")
        price = post.find(class_="result-price")
        url = post.find("a").get("href")
        
        if post.find(class_="result-image").get("data-ids"):
            image_id = post.find(class_="result-image").get("data-ids").split(":")[1].split(",")[0]
            image_url = BASE_CRAIGSLIST_IMAGE_URL.format(image_id)
        
        final_postings.append(
            (title.text if title is not None else "NO TITLE",
             price.text if price is not None else "FREE",
             url,
             image_url)
        )
    
    # Create context to send to client and render view.
    data_to_send = { 
        "search": search, 
        "final_postings": final_postings 
    }
    return render(request, 'my_app/new_search.html', data_to_send)