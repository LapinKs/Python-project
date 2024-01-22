from django.urls import path
from .views import *

urlpatterns = [
    path('', main_page, name='page'),
    path('relevance/', revelance_page, name='relevance'),
    path('geography/', geography_page, name='geography'),
    path('skills/', skillset_page, name='skills'),
    path('lastVacancy/', last_vacancies_page, name='lastVacancy'),
]

