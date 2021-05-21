import requests
from django.shortcuts import render,redirect
from threading import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
from datetime import datetime
from .models import Tour,City,categorie,Image,Depart,Operator,Subscriber,favourite
from aggregator.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def subscribe(request):
    if request.method == 'POST':
        if request.POST.get("email"):
            if Subscriber.objects.filter(email=request.POST["email"].lower()).exists():
                return home_page(request,"warning",request.POST["email"])
            else:
                s = Subscriber(None,request.POST["email"].lower())
                s.save()
            return home_page(request,True,request.POST["email"])

def newsletter_send(request):
    plaintext = get_template('email.html')
    htmly = get_template('email.html')
    tours = Tour.objects.all().order_by("?")
    d = {"principal":tours[0],"tours":tours[1:4]}
    subject, from_email = 'Checkout our new tours', EMAIL_HOST_USER
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    for subscriber in Subscriber.objects.all():
        msg = EmailMultiAlternatives(subject, text_content, from_email, [subscriber.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

def operators_page(request):
    op = Operator.objects.all()
    context = {"operator":op,}
    return render(request,"tour_operator.html",context)

def in_favourites(request , id):
    if request.user.is_authenticated:
        tour = Tour.objects.get(id=id)
        return favourite.objects.filter(tour=id,user=request.user.id).exists()
    return False


def remove_favourites(request, id):
    if in_favourites(request , id):
        favourite.objects.filter(tour=id,user=request.user.id).delete()
        return tour_page(request, id,False,False,True)
    return tour_page(request, id,False,False,False)


def add_favourites(request, id):
    if not in_favourites(request , id):
        f = favourite(None, id, request.user.id)
        f.save()
        return tour_page(request, id,True,True,False)
    return tour_page(request, id,True,False,False)

def home_page(request,subscription=False,email=None,logged_in=False,logged_out=False):
    cat = categorie.objects.all()
    op = Operator.objects.all()
    tours = Tour.objects.all().order_by("?")
    d1 = datetime.now().date()
    d2 = Depart.objects.all().order_by("-to_date").first().to_date
    context = {
        "title":"Voyage-ino",
        "categorie":cat, 
        "operator":op,
        "tours":tours[:8],
        "all_tours":tours.count()//10*10,
        "from_date":datetime.strftime(d1, "%m/%d/%Y"),
        "to_date":datetime.strftime(d2, "%m/%d/%Y"),
        "date_value":datetime.strftime(d1, "%m/%d/%Y"),
        "subscription":subscription,
        "email":email,
        "logged_in":logged_in,
        "logged_out":logged_out,
    }
    return render(request,"index.html",context)

def tour_page(request, id, favourite=None,added=False, removed=False):
    if favourite is None:
        favourite = in_favourites(request,id)
    context = {"tour":Tour.objects.get(id=id),"favourite":favourite,"added":added, "removed":removed}
    return render(request,"tour_detail.html",context)


def login_page(request,error=False,registration=False):
    if request.user.is_authenticated:
        return home_page(request)
    else:
        context={
            "error":error,
            "registration":registration
        }
        return render(request,"login.html",context)

def login_process(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return home_page(request, logged_in=True)
    else:
        return login_page(request, error=True)

def register(request,error=False):
    if request.user.is_authenticated:
        return home_page(request)
    else:
        context={
            "error":error,
        }
        return render(request,"register.html",context)

def register_process(request):
    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]
    if User.objects.filter(username=username).exists():
        return register(request,error=True)
    else:
        user = User.objects.create_user(username,email,password)
        user.save()
        return login_page(request,registration=True)

def logout_process(request):
    logout(request)
    return home_page(request,logged_out=True)

def page_not_found_view(request, exception=None):
    return render(request,"404.html")

def search(request,page=1):
    f = open("scraping.log","a+")
    print(request.GET, file=f)
    search = True
    if request.GET.get("page"):
        page = int(request.GET["page"])
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
        price_filter = Tour.objects.filter(price__gte=min_price, price__lte=max_price)
        duree_filter = Tour.objects.filter(duree__gte=min_duration,duree__lte=max_duration)
        results = price_filter & duree_filter
        if cities.count() == 1:
            cities_filter = cities[0].tour_set.all()
            results = results & cities_filter

        checked_categories = []
        checked_operator = []
        operators = []
        categories = []
        if request.GET.get("categories"):
            if request.GET["categories"] != ['[]']:
                categories = request.GET["categories"].split(",")
                for category in categories:
                    checked_categories.append(int(category))
                results = results & Tour.objects.filter(categorie__in=checked_categories)
        if request.GET.get("operators"):
            if request.GET["operators"] != ['[]']:
                operators = request.GET["operators"].split(",")
                for operator in operators:
                    checked_operator.append(int(operator))
                results = results & Tour.objects.filter(operator__in=checked_operator)
        #tri des resultats
        # par defaut price ASC
        if not request.GET.get("sort"):
            sort = "price"
        else:
            sort = request.GET["sort"]
        results = results.order_by(sort)
    

    #nous aurons besion de recuperer les parametres 
    link=[]
    for item in request.GET.items():
        link.append(item[0]+'='+item[1])
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
    #pagination
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

    context={
        'Tours':results[(page-1)*9:page*9],
        "cities":City.objects.all(),
        "operators": Operator.objects.all(),
        "checked_categories":checked_categories,
        "checked_operator":checked_operator,
        "checked_categories_value": ",".join(categories),
        "checked_operator_value": ",".join(operators),
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
        "destination": destination,
        "link":"&".join(link),
        "selected":selected,"suivant":suivant,"precedent":precedent,
        "pages":range(1 , nb+1)
        }
    return render(request,'tour_list.html',context)        

def get_operator(request, id, page=1):
    results = Operator.objects.get(id=id).tour_set.all()
    total = results.count()
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
    checked_operator = str(id)
    if not request.GET.get("sort"):
        sort = "price"
        sort_template= ""
    else:
        sort_template = sort = request.GET["sort"]
    results = results.order_by(sort)
    context={
        'Tours':results[9 * (page - 1):9 * page],
        "operators": Operator.objects.all(),
        "checked_operator":[id],
        "checked_operator_value":checked_operator,
        "pages":range(1 , nb+1),
        "selected":selected,
        "suivant":suivant,
        "precedent":precedent, 
        "operator": Operator.objects.get(id = id),
        "cities":City.objects.all(),
        "categories":categorie.objects.all(),
        "min_price":min_price,
        "max_price":max_price,
        "min_duration":min_duration,
        "max_duration":max_duration,
        "title":Operator.objects.get(id=id).name,
        "total":total,
        "from_date":d1.strftime("%m/%d/%Y"),
        "from_date_value":d1.strftime("%m/%d/%Y"),
        "to_date":d2.strftime("%m/%d/%Y"),
        "to_date_value":d2.strftime("%m/%d/%Y"),
        "min_price_value":min_price_value,
        "max_price_value":max_price_value,
        "min_duration_value":min_duration_value,
        "max_duration_value":max_duration_value,
        "sort_template":sort_template
        }
    return render(request,'tour_list.html',context)

def get_categorie(request, id,page=1):
    results = categorie.objects.get(id=id).tour_set.all()
    total = results.count()
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
    if not request.GET.get("sort"):
        sort = "price"
        sort_template=''
    else:
        sort_template = sort = request.GET["sort"]
    results = results.order_by(sort)
    context={
        'Tours':results[9 * (page - 1):9 * page],
        "operators": Operator.objects.all(),
        "cities":City.objects.all(),
        'categorie':categorie.objects.get(id=id),
        'categories':categorie.objects.all(),
        "pages":range(1 , nb+1),
        "selected":selected,"suivant":suivant,"precedent":precedent,
        "min_price":min_price,
        "max_price":max_price,
        "min_duration":min_duration,
        "max_duration":max_duration,
        "title":categorie.objects.get(id=id).name,
        "total":total,
        "from_date":d1.strftime("%m/%d/%Y"),
        "from_date_value":d1.strftime("%m/%d/%Y"),
        "to_date":d2.strftime("%m/%d/%Y"),
        "to_date_value":d2.strftime("%m/%d/%Y"),
        "checked_categories":[id],
        "checked_categories_value":str(id),
        "min_price_value":min_price_value,
        "max_price_value":max_price_value,
        "min_duration_value":min_duration_value,
        "max_duration_value":max_duration_value,
        "sort_template":sort_template
    }
    return render(request,'tour_list.html',context)

def update(request):
    if request.user.is_superuser:
        f = open("scraping.log","a+")
        print("starts in : ",datetime.now(), file=f, flush=True)
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
        tourradar_noce(request)
        tourradar_national(request)
        travlertalks(request,driver)
        print("ends in : ",datetime.now(), file=f,flush=True)
        driver.quit()
        T = Tour.objects.annotate(departs_count=Count("depart"))
        T.filter(departs_count=0).delete()
        T = Tour.objects.annotate(images_count=Count("image"))
        T.filter(images_count=0).delete()
        newsletter_send(request)
    context = {"scraping" : True}
    return render(request,"scraping.html",context)
    
def travlertalks(request,driver=None):
    travlertalks_national(request,driver)
    newsletter_send(request)
    return scraping(request, True)

def travlertalks_national(request,driver=None):
    f = open("scraping.log","a+")
    print("Travel Talks", file=f, flush=True)
    print("starts in : ",datetime.now(), file=f, flush=True)
    url='https://www.traveltalktours.com/search-tour/?_destination=morocco-tours'
    if driver == None:
        PATH = "C:\Program Files\chromedriver.exe"
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(PATH, options=options)
        tours = Tour.objects.filter(operator=3)
        for tour in tours:
            tour.image_set.all().delete()
            tour.depart_set.all().delete()
        tours.delete()
    driver.get(url)
    html = driver.execute_script("return document.documentElement.outerHTML")
    first_page = BeautifulSoup(html,"html.parser")
    deals = first_page.find_all("div",attrs={"class":"dest-tour-card"})
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
            t = Tour(None,url,title,price,str(details),duree,categorie,operator)
            t.save()
            #l'ajout des villes au voyage
            cities_list = soup.find_all("div",attrs={"class":"wp-block-columns sight-header-button"}) 
            for city in cities_list:
                if city.text.istitle():
                    city_name = city.div.h5.text.strip()
                if City.objects.filter(name=city_name).count() > 0:
                    t.cities.add(City.objects.filter(name=city_name).first())
                else:
                    c = City(None,city_name)
                    c.save()
                    t.cities.add(c)
            #l'ajout des images
            images_boxes = soup.find_all("li",attrs={"class":"blocks-gallery-item"})
            i = Image(None,t.id,first_image)
            i.save()  
            for image in images_boxes:
                url = image.img.get("src")
                i = Image(None,t.id,url)
                i.save()
            #l'ajout des departs
            departs_box = soup.find("div",attrs={"class":"wp-block-group alignwide date-rates-table hidden-mobile"})
            departs = departs_box.find_all("div",attrs={"class":"has-color-four-background-color"})
            for depart in departs[:-1]:
                infos = depart.find_all("div")
                from_date = datetime.strptime(infos[0].text.strip(),"%a %d %b %Y").date()
                to_date = datetime.strptime(infos[1].text.strip(),"%a %d %b %Y").date()
                price = infos[5].text.strip().split("€")[-1]
                d = Depart(None,t.id,from_date,to_date,price)
                d.save()
        except Exception as e:
            print(e, file=f)
            continue
    print("ends in : ",datetime.now(), file=f,flush=True)
    f.close()

def globus(request,driver=None):
    globus_international(request,driver)
    newsletter_send(request)
    return scraping(request, True)

def globus_international(request,driver=None):
    f = open("scraping.log","a+")
    print("Globus", file=f, flush=True)
    print("starts in : ",datetime.now(), file=f, flush=True)
    if driver == None:
            PATH = "C:\Program Files\chromedriver.exe"
            options = Options()
            options.headless = True
            driver = webdriver.Chrome(PATH, options=options)
            tours = Tour.objects.filter(operator=1)
            for tour in tours:
                tour.image_set.all().delete()
                tour.depart_set.all().delete()
            tours.delete()
    urls = ["https://www.globusjourneys.com/Vacation-Packages/Tour-Africa/Vacations/", "https://www.globusjourneys.com/Vacation-Packages/Tour-South-Pacific/Australia/","https://www.globusjourneys.com/Vacation-Packages/Tour-South-America/Central-America/"]
    for url in urls:
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
                t = Tour(None,lien,title,price,str(details),duree,categorie,operator)
                t.save()
                    # l'ajout des villes au voyage
                for city in cities_divs:
                    city = city.text.strip()
                    if City.objects.filter(name=city).count() > 0:
                        t.cities.add(City.objects.filter(name=city).first())
                    else:
                        c = City(None,city)
                        c.save()
                        t.cities.add(c)
                    # l'ajout des départs au voyage
                driver.get(lien+"?content=price")
                html = driver.execute_script("return document.documentElement.outerHTML")
                soup = BeautifulSoup(html,"html.parser")
                departs = soup.find_all("div",attrs={"class":"listing"})
                for depart in departs:
                    dates = depart.find_all("p",attrs={"class":"date-numbers"})
                    from_date = datetime.strptime(dates[0].text.strip(),"%d %b %y")
                    to_date = datetime.strptime(dates[1].text.strip(),"%d %b %y")
                    price = int("".join(depart.find("p",attrs={"class":"price-actual"}).text.split("$")[1].split(",")))
                    
                    d = Depart(None,t.id,from_date,to_date,price)
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
            
    print("ends in : ",datetime.now(), file=f,flush=True)
    f.close()

def intrepidtravel(request,driver=None):
    # intrepidtravel_international(request,driver)
    intrepidtravel_national(request,driver)
    newsletter_send(request)

    return scraping(request, True)

def intrepidtravel_international(request,driver=None): 
    f = open("scraping.log","a+")
    print("Intrepid Travel", file=f, flush=True)
    print("starts in : ",datetime.now(), file=f, flush=True)
    if driver == None:
        PATH = "C:\Program Files\chromedriver.exe"
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(PATH, options=options)
        tours = Tour.objects.filter(operator=2,categorie=2)
        for tour in tours:
            tour.image_set.all().delete()
            tour.depart_set.all().delete()
        tours.delete()
    urls = ["https://www.intrepidtravel.com/en/asia","https://www.intrepidtravel.com/en/central-america","https://www.intrepidtravel.com/en/north-america"]
    for url in urls:
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
                categorie = 2
                duree = int(soup.find("div", attrs={"class":"product-info__content"}).text)
                cities_group = soup.find("div",attrs={"class":"panel-group"}).find_all("h4",attrs={"class":"panel-title"})
                cities = []
                for city in cities_group:
                    cities.extend(re.split("/|-",city.a.text.strip().split(": ")[1].strip()))
                #creating tour
                t = Tour(None,url,title,price,str(details),duree,categorie,operator)
                t.save()
                # add cities to tour
                for city in cities:
                    city = city.strip()
                    if City.objects.filter(name=city).count() > 0:
                        t.cities.add(City.objects.filter(name=city).first())
                    else:
                        c = City(None,city)
                        c.save()
                        t.cities.add(c)
                #adding images to tour
                i = Image(None,t.id,first_image)
                i.save()
                for image in images:
                    i = Image(None,t.id,image)
                    i.save()
                #adding depatures to tip
                dates = soup.find_all("div",attrs={"class":"departure-info"})
                for date in dates:
                    from_date = datetime.strptime(date.div.find_all("div",attrs={"class":"col-sm-3"})[0].text.strip(),"%a %d %b %Y")
                    to_date = datetime.strptime(date.div.find_all("div",attrs={"class":"col-sm-3"})[1].text.strip(),"%a %d %b %Y")
                    price = int("".join(date.find("span",attrs={"class":"price-formatter"}).text.split("$")[1].split(",")))
                    d = Depart(None,t.id,from_date,to_date,price)
                    d.save()
            except Exception as e:
                print(e, file=f)
                
        print("ends in : ",datetime.now(), file=f,flush=True)
        f.close()

def intrepidtravel_national(request,driver=None): 
    f = open("scraping.log","a+")
    print("Intrepid Travel", file=f, flush=True)
    print("starts in : ",datetime.now(), file=f, flush=True)
    if driver == None:
        PATH = "C:\Program Files\chromedriver.exe"
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(PATH, options=options)
        tours = Tour.objects.filter(operator=2,categorie=1)
        for tour in tours:
            tour.image_set.all().delete()
            tour.depart_set.all().delete()
        tours.delete()
    url = "https://www.intrepidtravel.com/en/morocoo"
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
            t = Tour(None,url,title,price,str(details),duree,categorie,operator)
            t.save()
            # add cities to tour
            for city in cities:
                city = city.strip()
                if City.objects.filter(name=city).count() > 0:
                    t.cities.add(City.objects.filter(name=city).first())
                else:
                    c = City(None,city)
                    c.save()
                    t.cities.add(c)
            #adding images to tour
            i = Image(None,t.id,first_image)
            i.save()
            for image in images:
                i = Image(None,t.id,image)
                i.save()
            #adding depatures to tip
            dates = soup.find_all("div",attrs={"class":"departure-info"})
            for date in dates:
                from_date = datetime.strptime(date.div.find_all("div",attrs={"class":"col-sm-3"})[0].text.strip(),"%a %d %b %Y")
                to_date = datetime.strptime(date.div.find_all("div",attrs={"class":"col-sm-3"})[1].text.strip(),"%a %d %b %Y")
                price = int("".join(date.find("span",attrs={"class":"price-formatter"}).text.split("$")[1].split(",")))
                d = Depart(None,t.id,from_date,to_date,price)
                d.save()
        except Exception as e:
            print(e, file=f)
            
    print("ends in : ",datetime.now(), file=f,flush=True)
    f.close()

def touraddar(request):
    tourradar_noce(request)
    tourradar_national(request)
    newsletter_send(request)
    return scraping(request, True)

def tourradar_noce(request):
    f = open("scraping.log","a+")
    print("Tour Radar Honeymoon", file=f, flush=True)
    print("starts in : ",datetime.now(), file=f, flush=True)
    tours = Tour.objects.filter(operator=4,categorie=3)
    for tour in tours:
        tour.image_set.all().delete()
        tour.depart_set.all().delete()
    tours.delete()
    url="https://www.tourradar.com/sc/couples"
    response = requests.get(url)
    soup = BeautifulSoup(response.content,"html.parser")
    box = soup.find("section",attrs={"class":"ao-clp-serp-with-images ao-clp-serp-with-images--padding-top ah-grid-container"})
    countries = box.find_all("li",attrs={"class":"ao-clp-serp-with-images__item js-ao-clp-serp-with-images__item ah-grid-col ah-grid-col--s1-4 ah-grid-col--m1-4 ah-grid-col--l1-3"})
    for country in countries:
        url = "https://www.tourradar.com"+country.get("data-path")
        response = requests.get(url)
        first_page = BeautifulSoup(response.content,"html.parser")
        deals = first_page.find_all("li",attrs={"class":"tour exp"})
        f = open("scraping.log","a+")
        for deal in deals:    
            try:
                operator = 4
                url = "https://www.tourradar.com"+deal.a.get("href")
                title = deal.h4.text
                price = int("".join(deal.find("span",attrs={"class":"js-br__price-wrapper-price-description-value br__price-wrapper-price-description-value"}).text.split(",")))
                categorie = 3 #voyage de noce
                duree = deal.find("dd",{"class","br__price-wrapper-info-description"}).text.split()[0]
                response = requests.get(url)
                soup = BeautifulSoup(response.content,"html.parser") 
                details = str(soup.find("div",attrs={"class":"ao-tour-block","data-block-type":"Itinerary"}))
                #création du voyage
                t = Tour(None,url,title,price,str(details),duree,categorie, operator)
                t.save()

                #l'ajout des villes 
                cities = soup.find("div",{"class":"ao-tour-places-you-will-see__carousel"}).find_all("li") 
                for city in cities:
                    city = city.text.strip()
                    if City.objects.filter(name=city).count() > 0:
                        t.cities.add(City.objects.filter(name=city).first())
                    else:
                        id = City.objects.count() + 1
                        c = City(None,city.strip())
                        c.save()
                        t.cities.add(c)
                #l'ajout des images
                first_image = soup.find("div",{"class":"ao-tour-hero-image"}).img.get("src")
                i = Image(None.id,first_image)
                i.save()
                images_box = soup.find_all("img",attrs={"class":"ao-tour-places-you-will-see__image js-ao-tour-places-you-will-see__image"})
                for image in images_box:
                    i = Image(None,t.id,image.get("data-src"))
                    i.save()

                #l'ajout des departs
                departs_boxes = soup.find_all("li",attrs={"class":"am-tour-availability__variant"})
                for depart in departs_boxes:
                    from_date = datetime.strptime(depart.find("div",attrs={"class":"am-tour-availability__variant-bold-text"}).text.strip(),"%d %b, %Y")
                    to_date = datetime.strptime(depart.find("div",attrs={"class":"am-tour-availability__variant-bold-text--text-align-right"}).text.strip(),"%d %b, %Y")
                    price = int("".join(depart.find("div",attrs={"class":"am-tour-availability__variant-price-container"}).div.text.strip()[1:].split(",")))
                    d = Depart(None, t.id, from_date, to_date, price)
                    d.save()
            except Exception as e:
                print(e, file=f)
                continue
    print("ends in : ",datetime.now(), file=f,flush=True)
    f.close()

def tourradar_national(request):
    f = open("scraping.log","a+")
    print("Tour Radar National", file=f, flush=True)
    print("starts in : ",datetime.now(), file=f, flush=True)
    tours = Tour.objects.filter(operator=4,categorie=1)
    for tour in tours:
        tour.image_set.all().delete()
        tour.depart_set.all().delete()
    tours.delete()
    
    url='https://www.tourradar.com/d/morocco'
    response = requests.get(url)
    first_page = BeautifulSoup(response.content,"html.parser")
    deals = first_page.find_all("li",attrs={"class":"tour exp"})
    f = open("scraping.log","a+")
    for deal in deals:    
        try:
            operator = 4
            url = "https://www.tourradar.com"+deal.a.get("href")
            title = deal.h4.text
            price = int("".join(deal.find("span",attrs={"class":"js-br__price-wrapper-price-description-value br__price-wrapper-price-description-value"}).text.split(",")))
            categorie = 1 #voyage national
            duree = deal.find("dd",{"class","br__price-wrapper-info-description"}).text.split()[0]
            response = requests.get(url)
            soup = BeautifulSoup(response.content,"html.parser") 
            details = str(soup.find("div",attrs={"class":"ao-tour-block","data-block-type":"Itinerary"}))
            #création du voyage
            t = Tour(None,url,title,price,str(details),duree,categorie, operator)
            t.save()

            #l'ajout des villes 
            cities = soup.find("div",{"class":"ao-tour-places-you-will-see__carousel"}).find_all("li") 
            for city in cities:
                city = city.text.strip()
                if City.objects.filter(name=city).count() > 0:
                    t.cities.add(City.objects.filter(name=city).first())
                else:
                    id = City.objects.count() + 1
                    c = City(None,city.strip())
                    c.save()
                    t.cities.add(c)
            #l'ajout des images
            first_image = soup.find("div",{"class":"ao-tour-hero-image"}).img.get("src")
            i = Image(None,t.id,first_image)
            i.save()
            images_box = soup.find_all("img",attrs={"class":"ao-tour-places-you-will-see__image js-ao-tour-places-you-will-see__image"})
            for image in images_box:
                i = Image(None,t.id,image.get("data-src"))
                i.save()

            #l'ajout des departs
            departs_boxes = soup.find_all("li",attrs={"class":"am-tour-availability__variant"})
            for depart in departs_boxes:
                from_date = datetime.strptime(depart.find("div",attrs={"class":"am-tour-availability__variant-bold-text"}).text.strip(),"%d %b, %Y")
                to_date = datetime.strptime(depart.find("div",attrs={"class":"am-tour-availability__variant-bold-text--text-align-right"}).text.strip(),"%d %b, %Y")
                price = int("".join(depart.find("div",attrs={"class":"am-tour-availability__variant-price-container"}).div.text.strip()[1:].split(",")))
                d = Depart(None, t.id, from_date, to_date, price)
                d.save()
        except Exception as e:
            print(e, file=f)
            continue
    print("ends in : ",datetime.now(), file=f,flush=True)
    f.close()

def cosmos(request,driver=None):
    cosmos_international(request,driver)
    newsletter_send(request)
    return scraping(request, True)

def cosmos_international(request,driver=None):
    f = open("scraping.log","a+")
    print("Cosmos", file=f, flush=True)
    print("starts in : ",datetime.now(), file=f, flush=True)
    if driver == None:
            PATH = "C:\Program Files\chromedriver.exe"
            options = Options()
            options.headless = True
            driver = webdriver.Chrome(PATH, options=options)
            tours = Tour.objects.filter(operator=5)
            for tour in tours:
                tour.image_set.all().delete()
                tour.depart_set.all().delete()
            tours.delete()
    urls = ["https://www.cosmos.com/Vacations/Asia/", "https://www.cosmos.com/Vacations/South-Pacific/","https://www.cosmos.com/Vacations/South-America/"]
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        current_year = soup.find("div",attrs={"id":"current-year"})
        deals = current_year.find_all("div",attrs={"class":"product-listing-info"})
        for deal in deals:
            lien = deal.a.get("href")
            lien = "https://www.cosmos.com/"+lien
            try:
                operator = 5
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
                t = Tour(None,lien,title,price,str(details),duree,categorie,operator)
                t.save()
                    # l'ajout des villes au voyage
                for city in cities_divs:
                    city = city.text.strip()
                    if City.objects.filter(name=city).count() > 0:
                        t.cities.add(City.objects.filter(name=city).first())
                    else:
                        c = City(None,city)
                        c.save()
                        t.cities.add(c)
                    # l'ajout des départs au voyage
                driver.get(lien+"?content=price")
                html = driver.execute_script("return document.documentElement.outerHTML")
                soup = BeautifulSoup(html,"html.parser")
                departs = soup.find_all("div",attrs={"class":"listing"})
                print(lien+"?content=price", len(departs), file=f, flush=True)
                for depart in departs:
                    dates = depart.find_all("p",attrs={"class":"date-numbers"})
                    from_date = datetime.strptime(dates[0].text.strip(),"%d %b %y")
                    to_date = datetime.strptime(dates[1].text.strip(),"%d %b %y")
                    price = int("".join(depart.find("p",attrs={"class":"price-actual"}).text.split("$")[1].split(",")))
                    d = Depart(None,t.id,from_date,to_date,price)
                    d.save()
                # l'ajout des images
                i = Image(None,t.id,first_image)
                i.save()
                for image in images:
                    image = image.img.get("src")
                    i = Image(None,t.id,image)
                    i.save()
            except Exception as e:
                print(e, file=f, flush=True)
                continue
            
    print("ends in : ",datetime.now(), file=f,flush=True)
    f.close()

def scraping(request, scraping=False):   
    if request.user.is_superuser:
        context = {
            "operators":Operator.objects.all(),
            "categories":categorie.objects.all(),
            "scraping":scraping}
        return render(request, "scraping.html",context)
    else:
        return home_page(request)