from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import *
from .HeadHunterLoader import get_c_sharp_vacs
from .forms import DateForm
from datetime import date, timedelta


def index(request):
    context = {
        'title': "Главная страница",
        'chartPages': PageForCharts.objects.all()
    }
    return render(request, 'AboutCSharpDeveloper/index.html', context)


def show_page_for_chart(request, page_for_charts_slug):
    page_for_charts = PageForCharts.objects.get(slug=page_for_charts_slug)
    charts = Chart.objects.filter(page=page_for_charts.id)
    context = {
        'title': page_for_charts.name,
        'charts': charts,
        'chartPages': PageForCharts.objects.all(),
    }
    return render(request, 'AboutCSharpDeveloper/page_for_charts.html', context)


def show_chart(request, chart_slug):
    chart = Chart.objects.get(slug=chart_slug)
    context = {
        'title': chart.name,
        'chart': chart,
        'chartPages': PageForCharts.objects.all()
    }
    return render(request, 'AboutCSharpDeveloper/chart.html', context)


def recent_vacancies(request):
    context = {
        'title': "Последние вакансии",
        'chartPages': PageForCharts.objects.all(),
    }
    search_date = None
    vacs = None
    print('_________________Start_________________')
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            new_search_date = form.cleaned_data['date']
            if new_search_date == request.COOKIES.get('search_date'):
                form.add_error('date', 'Поиск по этой дате уже осуществлён')
            elif new_search_date >= date.today() or new_search_date <= date.today() - timedelta(30):
                form.add_error('date', 'Указана неверная дата')
            else:
                print('_________________FormIsValid_________________')
                vacs = get_c_sharp_vacs(new_search_date).to_dict('records')
                search_date = new_search_date
                print('_________________SearchEnd_________________')
    else:
        form = DateForm()
    context['form'] = form
    context['vacs'] = vacs

    html_page = render(request, 'AboutCSharpDeveloper/recent_vacancies.html', context)
    if search_date is not None:
        html_page.set_cookie('search_date', search_date)
    return html_page


# vacs = {}
# search_date = date(2023, 1, 1)


# def recent_vacancies(request):
#     global vacs
#     global search_date
#     context = {
#         'title': "Последние вакансии",
#         'chartPages': PageForCharts.objects.all()
#     }
#     if request.method == 'POST':
#         form = DateForm(request.POST)
#         if form.is_valid():
#             new_search_date = form.cleaned_data['date']
#             if new_search_date == search_date:
#                 form.add_error('date', 'Поиск по этой дате уже осуществлён')
#             else:
#                 search_date = new_search_date
#                 if search_date >= date.today() or search_date <= date.today() - timedelta(30):
#                     form.add_error('date', 'Указана неверная дата')
#                 else:
#                     vacs = get_c_sharp_vacs(search_date).to_dict('records')
#
#     else:
#         form = DateForm()
#     context['form'] = form
#     context['vacs'] = vacs
#     return render(request, 'AboutCSharpDeveloper/recent_vacancies.html', context)