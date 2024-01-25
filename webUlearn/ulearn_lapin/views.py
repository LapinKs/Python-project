from django.shortcuts import render
from .utils import *
from .api import HH_Api
import datetime
def main_page(request):
    return render(request,'Main_page.html',{'context':get_main_page()})

def geography_page(request):
    return render(request,'Geography.html',{'context':get_geography_page()})

def last_vacancies_page(request):
    vacancies = HH_Api('Специалист техподдержки').get_data_vacancies(datetime.datetime.now().strftime('%Y-%m-%d'), 10)
    return render(request,'Last_vacancies.html',{'context':vacancies})

def revelance_page(request):
    return render(request,'Relevance.html',{'context':get_relevance_page()})

def skillset_page(request):
    return render(request,'Skillset.html',{'context':get_skillset_page()})