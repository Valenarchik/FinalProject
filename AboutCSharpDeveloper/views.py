from django.http import HttpResponse
from django.shortcuts import render

menu = [
    {'title': 'Востребованность', 'url_name': 'relevance'},
    {'title': 'География', 'url_name': 'geography'},
    {'title': 'Навыки', 'url_name': 'skills'},
    {'title': 'Последние вакансии', 'url_name': 'recent_vacancies'},
]


def index(request):
    context = {
        'title': 'Главная',
        'menu': menu
    }
    return render(request, 'AboutCSharpDeveloper/index.html', context)


def relevance(request):
    return render(request, 'AboutCSharpDeveloper/relevance.html')


def geography(request):
    return render(request, 'AboutCSharpDeveloper/geography.html')


def skills(request):
    return render(request, 'AboutCSharpDeveloper/skills.html')


def recent_vacancies(request):
    return render(request, 'AboutCSharpDeveloper/recent_vacancies.html')
