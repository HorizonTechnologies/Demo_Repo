from django.shortcuts import render
import requests
from requests.compat import quote_plus
from selenium import webdriver  # https://chromedriver.storage.googleapis.com/index.html?path=80.0.3987.106/
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from . import models

BASE_NAUKAKRI_URL = 'https://www.naukri.com/{}-jobs'
BASE_NAUKAKRI_IMAGE_URL = 'https://img.naukimg.com/logo_images/v2/{}.gif'
BASE_MONSTERIND_URL = 'https://www.monsterindia.com/srp/results?query={}'
BASE_MONSTERIND_IMAGE_URL = ''
BASE_INDEED_URL = 'https://www.indeed.co.in/jobs?q={}&l=India&start='

# Create your views here.
def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    # print((quote_plus(search)))
    # search_url = BASE_MONSTERIND_URL.format(quote_plus(search))
    search_url_N = BASE_MONSTERIND_URL.format(quote_plus(search))
    search_url_M = BASE_NAUKAKRI_URL.format(quote_plus(search))
    search_url_I = BASE_INDEED_URL.format(quote_plus(search))
    print(search_url_N)
    print(search_url_M)
    print(search_url_I)

    options = Options()

    options.headless = True
    driver = webdriver.Chrome("/usr/bin/chromedriver", options=options)
    driver.set_page_load_timeout(10)
    driver.get(search_url_M)
    # response = driver.page_source
    # dataframe = pd.DataFrame(columns=["Title", "Location", "Posted", "Company", "Salary", "Description", "Apply URL"])
    find_posts = []

    for i in range(0, 2,10):

        # Step1: Get the page
        driver.get(search_url_I + str(i))
        driver.implicitly_wait(1)

        all_jobs = driver.find_elements_by_class_name('result')
        for job in all_jobs:

            result_html = job.get_attribute('innerHTML')
            soup = BeautifulSoup(result_html, 'html.parser')
            post_url = 'NONE'
            try:
                post_posted = soup.find(class_="date").text
            except:
                post_posted = 'None'

            try:
                post_title = soup.find("a", class_="jobtitle").text.replace('\n', '')
            except:
                post_title = 'None'

            try:
                post_location = soup.find(class_="location").text
            except:
                post_location = 'None'

            try:
                post_company = soup.find(class_="company").text.replace(
                    "\n", "").strip()
            except:
                post_company = 'None'

            try:
                post_salary = soup.find(class_="salary").text.replace("\n", "").strip()
            except:
                post_salary = 'None'

            sum_div = soup.find(class_="summary")
            # print(sum_div.text)
            try:
                close_button = driver.find_elements_by_class_name("popover-x-button-close")[0]
                close_button.click()
                post_job_desc = sum_div.text


            except:
                post_job_desc = sum_div.text
                print(post_job_desc)

            find_posts.append((post_title, post_url, post_location, post_posted, post_company, post_salary, post_job_desc))

    print(find_posts)
    dataframe = pd.DataFrame(
        columns=["Title", "Location", "Posted", "Company", "Salary", "Description", "Apply URL"])
    print((dataframe))
    dataframe.to_csv("results.csv", index=False)
    driver.quit()
    driver.close()

    # search_post_listing = soup.find("div", {"class": "card-apply-content"})  # Contains all the required data
    # print(search_post_listing)
    # for search_post in search_post_listing.findAll("div", {"class": "job-title"}):
    #     post = {}
    #     posts['TITLE'] = search_post.text
    #     print(search_post.text)
    #     posts.append(post)
    # df = pd.DataFrame(posts, columns=['Title'])
    # print(df)
    # print(posts)
    for_front_end = {
        'search': search,
        'final_posts': find_posts,
    }
    return render(request, 'apps/new_search.html', for_front_end)  # for_front_end
    driver.quit()
    driver.close()