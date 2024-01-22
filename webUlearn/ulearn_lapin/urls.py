from django.urls import path
from .views import *

urlpatterns = [
    path('', main_page, name='page'),
    path('revelance/', revelance_page, name='revelance'),
    path('geography/', geography_page, name='geography'),
    path('skills/', skillset_page, name='skills'),
    path('lastVacancy/', last_vacancies_page, name='lastVacancy'),
]