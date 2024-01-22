from django.shortcuts import render
import re
from datetime import datetime

def main_page(request):
    return render(request,'Main_page.html')

def geography_page(request):
    return render(request,'Geography.html')

def last_vacancies_page(request):
    return render(request,'Last_vacancies.html')

def revelance_page(request):
    return render(request,'Revelance.html')

def skillset_page(request):
    return render(request,'Skillset.html')