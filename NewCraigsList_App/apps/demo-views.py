## Implemented for Demo Purpose, works well!



from django.shortcuts import render
import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from . import models
import pandas as pd

# Demo Base URLs

BASE_CRAIGSLIST_URL = 'https://delhi.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_600x450.jpg'
BASE_DESC_URL = ''



# Create your views here.
def home(request):
    return render(request, 'base.html')


def new_search(request):

    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    # print((quote_plus(search)))
    search_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    # print(search_url)
    response = requests.get(search_url)
    data = response.text
    soup = BeautifulSoup(data, 'lxml')
    search_post_listing = soup.find_all('li', {'class': 'result-row'})

    find_posts = []

    for post in search_post_listing:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-date'):
            post_date = post.find(class_='result-date').text
        else:
            post_date = 'N/A'
        if post.find(class_='result-hood'):
            post_location = post.find(class_='result-hood').text
        else:
            post_location = 'N/A'
        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Flistonline.com.au%2Fwp-content%2Fuploads%2F2018%2F04%2Fno_image_ava.png&f=1&nofb=1'

        find_posts.append((post_title, post_url, post_date, post_location, post_image_url))

    print(find_posts)
    df = pd.DataFrame(find_posts, columns=['Title', 'URL', 'Date', 'Location', 'Image URL'])
    print(df)
    df.to_csv('results.csv')
    for_front_end = {
        'search': search,
        'final_posts': find_posts,
    }
    return render(request, 'apps/new_search.html', for_front_end)
from django.shortcuts import render
import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from . import models
import pandas as pd

# Demo Base URLs

# BASE_CRAIGSLIST_URL = 'https://delhi.craigslist.org/search/?query={}'
# BASE_IMAGE_URL = 'https://images.craigslist.org/{}_600x450.jpg'
# BASE_DESC_URL = ''

# Actual URLs

BASE_NAUKAKRI_URL = 'https://www.naukri.com/{}-jobs?k={}'
BASE_NAUKAKRI_IMAGE_URL = ''
BASE_MONSTERIND_URL = 'https://www.monsterindia.com/srp/results?query={}'
BASE_MONSTERIND_IMAGE_URL = ''

# Create your views here.
def home(request):
    return render(request, 'base.html')


def new_search(request):

    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    # print((quote_plus(search)))
    search_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    # print(search_url)
    response = requests.get(search_url)
    data = response.text
    soup = BeautifulSoup(data, 'lxml')
    search_post_listing = soup.find_all('li', {'class': 'result-row'})

    find_posts = []

    for post in search_post_listing:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-date'):
            post_date = post.find(class_='result-date').text
        else:
            post_date = 'N/A'
        if post.find(class_='result-hood'):
            post_location = post.find(class_='result-hood').text
        else:
            post_location = 'N/A'
        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Flistonline.com.au%2Fwp-content%2Fuploads%2F2018%2F04%2Fno_image_ava.png&f=1&nofb=1'

        find_posts.append((post_title, post_url, post_date, post_location, post_image_url))

    print(find_posts)
    df = pd.DataFrame(find_posts, columns=['Title', 'URL', 'Date', 'Location', 'Image URL'])
    print(df)
    df.to_csv('results.csv')
    for_front_end = {
        'search': search,
        'final_posts': find_posts,
    }
    return render(request, 'apps/new_search.html', for_front_end)
