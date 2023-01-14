from django.http import HttpResponse
from django.shortcuts import render
from HeadHunterLoader import get_c_sharp_vacs

menu = [
    {'title': 'Востребованность', 'url_name': 'relevance'},
    {'title': 'География', 'url_name': 'geography'},
    {'title': 'Навыки', 'url_name': 'skills'},
    {'title': 'Последние вакансии', 'url_name': 'recent_vacancies'},
]


def index(request):
    context = {
        'menu': menu
    }
    return render(request, 'AboutCSharpDeveloper/index.html', context)


def relevance(request):
    context = {
        'menu': menu
    }
    return render(request, 'AboutCSharpDeveloper/relevance.html', context)


def geography(request):
    return render(request, 'AboutCSharpDeveloper/geography.html')


def skills(request):
    return render(request, 'AboutCSharpDeveloper/skills.html')


def recent_vacancies(request):
    vacs = get_c_sharp_vacs(2022, 12, 20)
    return render(request, 'AboutCSharpDeveloper/recent_vacancies.html')
