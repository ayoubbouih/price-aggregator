import requests
from django.shortcuts import render 
from threading import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = "https://monograms.com/booking/monograms/packages.aspx?region=europe"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
deals = soup.find_all("div",attrs={"class":"listing-contain"})
f = open("monogram.txt", "a+")
for deal in deals:
    url = deal.find("a",attrs={"class","yourway_button_details_ml"}).get("href")
    print(url)