from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import *


def index(request):
    chartPages = PageForCharts.objects.all()
    context = {
        'chartPages': chartPages
    }
    return render(request, 'AboutCSharpDeveloper/index.html', context)


def show_page_for_chart(request, page_for_charts_slug):
    chartPages = PageForCharts.objects.all()
    page_for_charts_id = PageForCharts.objects.get(slug=page_for_charts_slug).id
    charts = Chart.objects.filter(page=page_for_charts_id)
    context = {
        'charts': charts,
        'chartPages': chartPages,
    }
    return render(request, 'AboutCSharpDeveloper/page_for_charts.html', context)


def show_chart(request, chart_slug):
    return HttpResponse(f'Страница с графиком {chart_slug}')


def recent_vacancies(request):
    # vacs = get_c_sharp_vacs(2022, 12, 20)
    chartPages = PageForCharts.objects.all()
    context = {
        'chartPages': chartPages
    }
    return render(request, 'AboutCSharpDeveloper/recent_vacancies.html', context)
