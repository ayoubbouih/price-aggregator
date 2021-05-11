import requests
from django.shortcuts import render 
from django.http import HttpResponse 
from django.contrib.sessions.backends.db import SessionStore
from threading import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options
import re
from datetime import datetime
from .models import Tour,City,categorie,Review,Image,Depart,Operator
from django.db.models import Count

def get_favourites(request):
    if "fav" in request.COOKIES:
        fav = request.COOKIES["fav"]
        response =  render(request, "cookies.html", {"fav":fav})
        response.set_cookie("fav",request.COOKIES["fav"]+","+fav)
    else:
        fav = 0
        response =  render(request, "cookies.html", {"fav":fav})
        response.set_cookie("fav",str(int(fav) + 1))
    return response

def home_page(request):
    cat = categorie.objects.all()
    op = Operator.objects.all()
    tours = Tour.objects.all().order_by("?")
    cities = City.objects.all()
    d1 = datetime.now().date()
    d2 = Depart.objects.all().order_by("-to_date").first().to_date
    context = {
        "title":"Voyage-ino",
        "categorie":cat, 
        "operator":op,
        "tours":tours[:8],
        "from_date":datetime.strftime(d1, "%m/%d/%Y"),
        "to_date":datetime.strftime(d2, "%m/%d/%Y"),
        "date_value":datetime.strftime(d1, "%m/%d/%Y")

    }
    return render(request,"index.html",context)

def tour_page(request, id):
    context = {"tour":Tour.objects.get(id=id)}
    return render(request,"tour_detail.html",context)

def operator_page(request):
    op = Operator.objects.all()
    context = {"operator":op,}
    return render(request,"tour_operator.html",context)


def page_not_found_view(request, exception=None):
    return render(request,"404.html")

def search(request,page=1):
    f = open("scraping.log","a+")
    print(request.GET, file=f)
    search = True
    checked = ""
    if request.GET["destination"]:
        destination = request.GET["destination"]
        city_name = str(request.GET["destination"]).capitalize()
        if City.objects.filter(name=city_name).exists():
            cities = City.objects.filter(name=city_name)
        else:
            results=[]
            search=False
    else:
        destination = ""
        cities = City.objects.all()
    print(cities, file=f)
    if request.GET.get("min_price"):
        min_price = int(request.GET["min_price"][1:])
        max_price = int(request.GET["max_price"][1:])
    else:
        min_price = Tour.objects.all().order_by("price").first().price
        max_price = Tour.objects.all().order_by("price").last().price

    if request.GET.get("from_date") and request.GET.get("to_date"):
        date_min = datetime.strptime(request.GET["from_date"],"%m/%d/%Y").date()
        date_max = datetime.strptime(request.GET["to_date"],"%m/%d/%Y").date()
    else:
        date_min = datetime.now().date()
        date_max = Depart.objects.all().order_by("-to_date").first().to_date

    if request.GET.get("min_duration"):
        min_duration = int(request.GET["min_duration"].split()[0])
        max_duration = int(request.GET["max_duration"].split()[0])
    else:
        min_duration = Tour.objects.all().order_by("duree").first().duree
        max_duration = Tour.objects.all().order_by("duree").last().duree
    if search is not False:
        tmp = []
        checked = []
        if request.GET.get("categories"):
            if request.GET["categories"] != ['[]']:
                categories = request.GET["categories"].split(",")
                for category in categories:
                    checked.append(category)
                    id = int(category)
                    tours = categorie.objects.get(id=id).tour_set.all()
                    tmp.extend(tours.filter(price__gte=min_price, price__lte=max_price,duree__gte=min_duration,duree__lte=max_duration))
                    results=[]
                    for tour in tmp:
                        if tour.depart_set.filter(from_date__gte=date_min,to_date__lte=date_max).count() != 0 and cities.intersection(cities,tour.cities.all()).count():
                            results.append(tour)
                checked=",".join(checked)
            else:
                tmp = Tour.objects.filter(price__gte=min_price, price__lte=max_price,duree__gte=min_duration,duree__lte=max_duration)
                results=[]
                for tour in tmp:
                    print("here",cities, cities.intersection(cities,tour.cities.all()).count() , file=f)
                    if tour.depart_set.filter(from_date__gte=date_min,to_date__lte=date_max).count() != 0 and cities.intersection(cities,tour.cities.all()).count():
                        results.append(tour)
        else:
            tmp = Tour.objects.filter(price__gte=min_price, price__lte=max_price,duree__gte=min_duration,duree__lte=max_duration)
            results=[]
            for tour in tmp:
                if tour.depart_set.filter(from_date__gte=date_min,to_date__lte=date_max).count() != 0 and cities.intersection(cities,tour.cities.all()).count():
                    results.append(tour)
    total = len(results)
    from_date = datetime.now().date()
    from_date_value = datetime.strftime(date_min, "%m/%d/%Y")
    to_date = Depart.objects.all().order_by("-to_date").first().to_date
    to_date_value = datetime.strftime(date_max, "%m/%d/%Y")
    min_price_value = min_price
    max_price_value =max_price
    min_price = Tour.objects.all().order_by("price").first().price
    max_price = Tour.objects.all().order_by("price").last().price
    min_duration_value = min_duration
    max_duration_value = max_duration
    min_duration = Tour.objects.all().order_by("duree").first().duree
    max_duration = Tour.objects.all().order_by("duree").last().duree
    context={
        'Tours':results,
        "cities":City.objects.all(),
        "checked":checked,
        'categories':categorie.objects.all(),
        "min_price":min_price,"max_price":max_price,
        "min_price_value":min_price_value,"max_price_value":max_price_value,
        "min_duration":min_duration,"max_duration":max_duration,
        "min_duration_value":min_duration_value,"max_duration_value":max_duration_value,
        "title":"search results","total":total,
        "from_date":from_date.strftime("%m/%d/%Y"),
        "to_date":to_date.strftime("%m/%d/%Y"),
        "to_date_value":to_date_value,
        "from_date_value":from_date_value,
        "destination": destination
        }
    return render(request,'search-results.html',context)        

def get_city(request, id, page=1):
    nb = City.objects.get(id=id).tour_set.count() // 9 + 1
    if nb > 1:
        selected = page
        if selected == 1:
            precedent = None
        else:
            precedent = selected - 1
        if selected == nb:
            suivant = None
        else:
            suivant = selected + 1
    else:
        suivant = None
        precedent = None
        selected = None
    context = {'Tours':City.objects.get(id=id).tour_set.all()[9 * (page - 1):9 * page],"pages":range(1 , nb+1),"selected":selected,"suivant":suivant,"precedent":precedent, 'city': City.objects.get(id = id),"cities":City.objects.all(),"categories":categorie.objects.all()}
    return render(request,'tour_list.html',context)

def get_operator(request, id, page=1):
    total = Operator.objects.get(id=id).tour_set.count()
    nb = total // 9 + 1
    if nb > 1:
        selected = page
        if selected == 1:
            precedent = None
        else:
            precedent = selected - 1
        if selected == nb:
            suivant = None
        else:
            suivant = selected + 1
    else:
        suivant = None
        precedent = None
        selected = None

    min_price = Tour.objects.all().order_by("price").first().price
    min_price_value = Operator.objects.get(id=id).tour_set.all().order_by("price").first().price
    max_price = Tour.objects.all().order_by("price").last().price
    max_price_value = Operator.objects.get(id=id).tour_set.all().order_by("price").last().price
    min_duration = Tour.objects.all().order_by("duree").first().duree
    max_duration = Tour.objects.all().order_by("duree").last().duree
    min_duration_value = Operator.objects.get(id=id).tour_set.all().order_by("duree").first().duree
    max_duration_value = Operator.objects.get(id=id).tour_set.all().order_by("duree").last().duree
    d1 = datetime.now().date()
    d2 = Depart.objects.all().order_by("-to_date").first().to_date

    context = {
        "Tours":Operator.objects.get(id=id).tour_set.all()[9 * (page - 1):9 * page],
        "pages":range(1 , nb+1),
        "selected":selected,
        "suivant":suivant,
        "precedent":precedent, 
        "operator": Operator.objects.get(id = id),
        "cities":City.objects.all(),
        "categories":categorie.objects.all(),
        "min":min_price,
        "max":max_price,
        "min_duration":min_duration,
        "max_duration":max_duration,
        "title":Operator.objects.get(id=id).name,
        "total":total,
        "from_date":d1.strftime("%m/%d/%Y"),
        "to_date":d2.strftime("%m/%d/%Y"),
        "min_price_value":min_price_value,
        "max_price_value":max_price_value,
        "min_duration_value":min_duration_value,
        "max_duration_value":max_duration_value,
        }
    return render(request,'tour_list_op.html',context)

def get_categorie(request, id,page=1):
    total = categorie.objects.get(id=id).tour_set.count()
    nb = total // 9 + 1
    if nb > 1:
        selected = page

        if selected == 1:
            precedent = None
        else:
            precedent = selected - 1

        if selected == nb:
            suivant = None
        else:
            suivant = selected + 1
    else:
        suivant = None
        precedent = None
        selected = None
    min_price = Tour.objects.all().order_by("price").first().price
    min_price_value = categorie.objects.get(id=id).tour_set.all().order_by("price").first().price
    max_price = Tour.objects.all().order_by("price").last().price
    max_price_value = categorie.objects.get(id=id).tour_set.all().order_by("price").last().price
    min_duration = Tour.objects.all().order_by("duree").first().duree
    max_duration = Tour.objects.all().order_by("duree").last().duree
    min_duration_value = categorie.objects.get(id=id).tour_set.all().order_by("duree").first().duree
    max_duration_value = categorie.objects.get(id=id).tour_set.all().order_by("duree").last().duree
    d1 = datetime.now().date()
    d2 = Depart.objects.all().order_by("-to_date").first().to_date
    context={
        'Tours':categorie.objects.get(id=id).tour_set.all()[9 * (page - 1):9 * page],
        "cities":City.objects.all(),
        'categorie':categorie.objects.get(id=id),
        'categories':categorie.objects.all(),
        "pages":range(1 , nb+1),
        "selected":selected,"suivant":suivant,"precedent":precedent,
        "min_price":min_price,"max_price":max_price,
        "min_duration":min_duration,"max_duration":max_duration,
        "title":categorie.objects.get(id=id).name,"total":total,
        "from_date":d1.strftime("%m/%d/%Y"),
        "to_date":d2.strftime("%m/%d/%Y"),
        "checked":[id],
        "min_price_value":min_price_value,
        "max_price_value":max_price_value,
        "min_duration_value":min_duration_value,
        "max_duration_value":max_duration_value,
    }
    return render(request,'tour_list.html',context)

def update(request):
    f = open("scraping.log","a+")
    print("starts in : ",datetime.datetime.now(), file=f, flush=True)
    Tour.objects.all().delete()
    Image.objects.all().delete()
    Depart.objects.all().delete()
    City.objects.all().delete()
    PATH = "C:\Program Files\chromedriver.exe"
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(PATH, options=options)
    globus(request,driver)
    intrepidtravel(request,driver)
    tourradar(request)
    travlertalks(request,driver)
    print("ends in : ",datetime.datetime.now(), file=f,flush=True)
    driver.quit()
    
def travlertalks(request,driver=None):
    url='https://www.traveltalktours.com/search-tour/?_destination=morocco-tours'
    driver.get(url)
    html = driver.execute_script("return document.documentElement.outerHTML")
    first_page = BeautifulSoup(html,"html.parser")
    deals = first_page.find_all("div",attrs={"class":"dest-tour-card"})
    f = open("scraping.log","a+")
    for deal in deals:
        try:
            operator = 3
            title = deal.h4.text
            url = deal.figure.a.get("href")
            duree= int(deal.h5.text.split()[0])
            price = int(deal.find("p",attrs={"class","has-text-align-right has-color-two-color has-text-color"}).text.strip()[1:])
            first_image = deal.figure.a.img.get("src")
            categorie = 1 #national
            response = requests.get(url)
            soup = BeautifulSoup(response.content,"html.parser")
            details = str(soup.find("div",attrs={"id":"itinerary"}))
            # création du voyage
            if Tour.objects.count() == 0:
                id = 1
            else:
                id = Tour.objects.latest('id').id + 1
            t = Tour(id,url,title,price,str(details),duree,categorie,operator)
            t.save()
            #l'ajout des villes au voyage
            cities_list = soup.find_all("div",attrs={"class":"wp-block-columns sight-header-button"}) 
            for city in cities_list:
                if city.text.istitle():
                    city_name = city.div.h5.text.strip()
                if City.objects.filter(name=city_name).count() > 0:
                    t.cities.add(City.objects.filter(name=city_name).first())
                else:
                    id = City.objects.count() + 1
                    c = City(id,city_name)
                    c.save()
                    t.cities.add(c)
            #l'ajout des images
            images_boxes = soup.find_all("li",attrs={"class":"blocks-gallery-item"})
            if Image.objects.count() == 0:
                id = 1
            else:
                id = Image.objects.latest('id').id + 1
            i = Image(id,t.id,first_image)
            i.save()  
            for image in images_boxes:
                url = image.img.get("src")
                id = Image.objects.latest('id').id + 1
                i = Image(id,t.id,url)
                i.save()
            #l'ajout des departs
            departs_box = soup.find("div",attrs={"class":"wp-block-group alignwide date-rates-table hidden-mobile"})
            departs = departs_box.find_all("div",attrs={"class":"has-color-four-background-color"})
            for depart in departs[:-1]:
                infos = depart.find_all("div")
                from_date = datetime.datetime.strptime(infos[0].text.strip(),"%a %d %b %Y").date()
                to_date = datetime.datetime.strptime(infos[1].text.strip(),"%a %d %b %Y").date()
                price = infos[5].text.strip().split("€")[-1]
                if Depart.objects.count() == 0:
                    id = 1
                else:
                    id = Depart.objects.latest('id').id + 1
                d = Depart(id,t.id,from_date,to_date,price)
                d.save()
        except Exception as e:
            print(e, file=f)
            continue
    f.close()

def globus(request,driver=None):
    f = open("scraping.log","a+")
    url="https://www.globusjourneys.com/Vacation-Packages/Tour-Africa/Vacations/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    current_year = soup.find("div",attrs={"id":"current-year"})
    deals = current_year.find_all("div",attrs={"class":"product-listing-info"})
    for deal in deals:
        lien = deal.a.get("href")
        lien = "https://www.globusjourneys.com"+lien
        try:
            operator = 1
            driver.get(lien)
            html = driver.execute_script("return document.documentElement.outerHTML")
            soup = BeautifulSoup(html,"html.parser")
            title = soup.find("p",attrs={"id":"product-name"}).text
            first_image = soup.find("div",attrs={"class":"vacation-hero-photo"}).get("style").split("'")[1]
            images = soup.find_all("li",attrs={"class":"tft-slim-carousel-item"})
            categorie = 2 #international
            price = int("".join(soup.find("span",attrs={"class":"price"}).text[1:].split(",")))
            cities_divs = soup.find("div",attrs={"id":"mapsButtons"}).find_all("div")
            duree = int(soup.find("p",attrs={"id":"product-description"}).text.strip().split()[0])
            details = soup.find("div",attrs={"id":"itinerary"})
            # création du voyage
            if Tour.objects.count() == 0:
                id = 1
            else:
                id = Tour.objects.latest('id').id + 1
            t = Tour(id,lien,title,price,str(details),duree,categorie,operator)
            t.save()
                # l'ajout des villes au voyage
            for city in cities_divs:
                city = city.text.strip()
                if City.objects.filter(name=city).count() > 0:
                    t.cities.add(City.objects.filter(name=city).first())
                else:
                    id = City.objects.count() + 1
                    c = City(id,city)
                    c.save()
                    t.cities.add(c)
                # l'ajout des départs au voyage
            driver.get(lien+"?content=price")
            html = driver.execute_script("return document.documentElement.outerHTML")
            soup = BeautifulSoup(html,"html.parser")
            departs = soup.find_all("div",attrs={"class":"listing"})
            for depart in departs:
                dates = depart.find_all("p",attrs={"class":"date-numbers"})
                from_date = datetime.datetime.strptime(dates[0].text.strip(),"%d %b %y")
                to_date = datetime.datetime.strptime(dates[1].text.strip(),"%d %b %y")
                price = int("".join(depart.find("p",attrs={"class":"price-actual"}).text.split("$")[1].split(",")))
                if Depart.objects.count() == 0:
                    id = 1
                else:
                    id = Depart.objects.latest('id').id + 1
                d = Depart(id,t.id,from_date,to_date,price)
                d.save()
            # l'ajout des images
            if Image.objects.count() == 0:
                id = 1
            else:
                id = Image.objects.latest('id').id + 1
            i = Image(id,t.id,first_image)
            i.save()
            for image in images:
                image = image.img.get("src")
                id = Image.objects.latest('id').id + 1
                i = Image(id,t.id,image)
                i.save()
        except Exception as e:
            print(e, file=f, flush=True)
            continue
        f.close()
    return render(request,"index.html")

def intrepidtravel(request,driver=None): 
    url = "https://www.intrepidtravel.com/en/morocco"
    if driver == None:
        PATH = "C:\Program Files\chromedriver.exe"
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(PATH, options=options)
    driver.get(url)
    html = driver.execute_script("return document.documentElement.outerHTML")
    first_page = BeautifulSoup(html,"html.parser")
    deals = first_page.find_all("div", attrs={"class":"card-product--map"})
    f = open("scraping.log","a+")
    for deal in deals:
        try:
            operator = 2
            url = deal.find("div",attrs={"class":"card-product__image"}).find("a").get("href")
            url = "https://www.intrepidtravel.com"+url
            driver.get(url)
            html = driver.execute_script("return document.documentElement.outerHTML")
            soup = BeautifulSoup(html,"html.parser")
            title = soup.find("div",attrs={"class":"banner__content"}).find("h1", attrs={"class":"banner__heading"}).text
            price = int(soup.find("span", attrs={"class":"price-formatter"}).get("price-value"))
            details = soup.find("div", attrs={"class":"panel-group"})
            first_image = soup.find("div", attrs={"class":"image-placeholder"}).find("img").get("src")
            slider = soup.find("div",attrs={"class":"slick-track"})
            images = slider.find_all("img")
            images = [image.get("data-src") for image in images]
            categorie = 1
            duree = int(soup.find("div", attrs={"class":"product-info__content"}).text)
            cities_group = soup.find("div",attrs={"class":"panel-group"}).find_all("h4",attrs={"class":"panel-title"})
            cities = []
            for city in cities_group:
                cities.extend(re.split("/|-",city.a.text.strip().split(": ")[1].strip()))
            #creating tour
            if Tour.objects.count() == 0:
                id = 1
            else:
                id = Tour.objects.latest('id').id + 1
            t = Tour(id,url,title,price,str(details),duree,categorie,operator)
            t.save()
            # add cities to tour
            for city in cities:
                city = city.strip()
                if City.objects.filter(name=city).count() > 0:
                    t.cities.add(City.objects.filter(name=city).first())
                else:
                    id = City.objects.count() + 1
                    c = City(id,city)
                    c.save()
                    t.cities.add(c)
            #adding images to tour
            if Image.objects.count() == 0:
                id = 1
            else:
                id = Image.objects.latest('id').id + 1
            i = Image(id,t.id,first_image)
            i.save()
            for image in images:
                id = Image.objects.latest('id').id + 1
                i = Image(id,t.id,image)
                i.save()
            #adding depatures to tip
            dates = soup.find_all("div",attrs={"class":"departure-info"})
            for date in dates:
                from_date = datetime.strptime(date.div.find_all("div",attrs={"class":"col-sm-3"})[0].text.strip(),"%a %d %b %Y")
                to_date = datetime.strptime(date.div.find_all("div",attrs={"class":"col-sm-3"})[1].text.strip(),"%a %d %b %Y")
                price = int("".join(date.find("span",attrs={"class":"price-formatter"}).text.split("$")[1].split(",")))
                if Depart.objects.count() == 0:
                    id = 1
                else:
                    id = Depart.objects.latest('id').id + 1
                d = Depart(id,t.id,from_date,to_date,price)
                d.save()
        except Exception as e:
            print(e, file=f)
            
        print(url, "cities:", len(cities), "images:",len(images), "departs:",len(dates), file=f ,flush=True)
    f.close()

def tourradar(request):
    url='https://www.tourradar.com/d/morocco'
    response = requests.get(url)
    first_page = BeautifulSoup(response.content,"html.parser")
    deals = first_page.find_all("li",attrs={"class":"tour exp"})
    f = open("scraping.log","a+")
    for deal in deals:    
        try:
            url = "https://www.tourradar.com"+deal.a.get("href")
            title = deal.h4.text
            price = int("".join(deal.find("span",attrs={"class":"js-br__price-wrapper-price-description-value br__price-wrapper-price-description-value"}).text.split(",")))
            categorie = 3 #voyage de noce
            duree = deal.find("dd",{"class","br__price-wrapper-info-description"}).text.split()[0]
            response = requests.get(url)
            soup = BeautifulSoup(response.content,"html.parser") 
            details = str(soup.find("div",attrs={"class":"ao-tour-block","data-block-type":"Itinerary"}))
            #création du voyage

            if Tour.objects.count() == 0:
                id = 1
            else:
                id = Tour.objects.latest('id').id + 1
            t = Tour(id,url,title,price,str(details),duree,categorie)
            t.save()

            #l'ajout des villes 
            if City.objects.count() == 0:
                id = 1
            else:
                id = City.objects.latest('id').id + 1
            cities = soup.find("div",{"class":"ao-tour-places-you-will-see__carousel"}).find_all("li") 
            for city in cities:
                city = city.text.strip()
                if City.objects.filter(name=city).count() > 0:
                    t.cities.add(City.objects.filter(name=city).first())
                else:
                    id = City.objects.count() + 1
                    c = City(id,city.strip())
                    c.save()
                    t.cities.add(c)
            #l'ajout des images
            first_image = soup.find("div",{"class":"ao-tour-hero-image"}).img.get("src")
            id = Image.objects.latest('id').id + 1
            i = Image(id,t.id,first_image)
            i.save()
            images_box = soup.find_all("img",attrs={"class":"ao-tour-places-you-will-see__image js-ao-tour-places-you-will-see__image"})
            for image in images_box:
                id = Image.objects.latest('id').id + 1
                i = Image(id,t.id,image.get("data-src"))
                i.save()

            #l'ajout des departs
            departs_boxes = soup.find_all("li",attrs={"class":"am-tour-availability__variant"})
            for depart in departs_boxes:
                from_date = datetime.datetime.strptime(depart.find("div",attrs={"class":"am-tour-availability__variant-bold-text"}).text.strip(),"%d %b, %Y")
                to_date = datetime.datetime.strptime(depart.find("div",attrs={"class":"am-tour-availability__variant-bold-text--text-align-right"}).text.strip(),"%d %b, %Y")
                price = int("".join(depart.find("div",attrs={"class":"am-tour-availability__variant-price-container"}).div.text.strip()[1:].split(",")))
                id = Depart.objects.latest('id').id + 1
                d = Depart(id, t.id, from_date, to_date, price)
                d.save()
        except Exception as e:
            print(e, file=f)
            continue
    f.close()