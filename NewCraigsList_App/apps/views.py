from django.shortcuts import render
import requests
from requests.compat import quote_plus
from selenium import webdriver  #https://chromedriver.storage.googleapis.com/index.html?path=80.0.3987.106/
from bs4 import BeautifulSoup
from . import models
import pandas as pd

BASE_NAUKAKRI_URL = 'https://www.naukri.com/{}-jobs'
BASE_NAUKAKRI_IMAGE_URL = 'https://img.naukimg.com/logo_images/v2/{}.gif'
BASE_MONSTERIND_URL = 'https://www.monsterindia.com/srp/results?query={}'
BASE_MONSTERIND_IMAGE_URL = ''


# Create your views here.
def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    # print((quote_plus(search)))
    # search_url = BASE_MONSTERIND_URL.format(quote_plus(search))
    search_url_N = BASE_NAUKAKRI_URL.format(quote_plus(search))
    search_url_M = BASE_MONSTERIND_URL.format(quote_plus(search))
    print(search_url_N)
    print(search_url_M)
    driver = webdriver.Chrome("/home/my/Downloads/chromedriver_linux64/chromedriver") #include full download directory of chromedriver
    driver.get(search_url_M)
    response = driver.page_source
    #print(search_url)
    # response = requests.get(search_url)
    
    # print(response)
    soup = BeautifulSoup(response, 'lxml')
    
    search_post_listing = soup.find("div", {"class": "card-apply-content"}) #Contains all the required data
    print(search_post_listing) 
    posts = []
    # for search_post in search_post_listing.findAll("div", {"class": "job-title"}):
    #     post = {}
    #     posts['TITLE'] = search_post.text
    #     print(search_post.text)
    #     posts.append(post)
    #df = pd.DataFrame(posts, columns=['Title'])
    #print(df)
    print(posts)
    for_front_end = {
        'search': search,
        #'final_posts': find_posts,
    }
    return render(request, 'apps/new_search.html', for_front_end)  # for_front_end
