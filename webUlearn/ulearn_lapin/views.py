from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

def main_page(request):
    return render(request,'templates/Main_page.html')

def geography_page(request):
    return render(request,'templates/Geography.html')

def last_vacancies_page(request):
    return render(request,'templates/Last_vacancies.html')

def revelance_page(request):
    return render(request,'templates/Revelance.html')

def skillset_page(request):
    return render(request,'templates/Skillset.html')