from .models import *
def get_main_page():
    return MainPage.objects.all()


def get_relevance_page():
    return Relevance.objects.all()


def get_geography_page():
    return Geography.objects.all()


def get_skillset_page():
    return Skillset.objects.all()