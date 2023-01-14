from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import *
from .HeadHunterLoader import get_c_sharp_vacs


def index(request):
    context = {
        'chartPages': PageForCharts.objects.all()
    }
    return render(request, 'AboutCSharpDeveloper/index.html', context)


def show_page_for_chart(request, page_for_charts_slug):
    page_for_charts_id = PageForCharts.objects.get(slug=page_for_charts_slug).id
    charts = Chart.objects.filter(page=page_for_charts_id)
    context = {
        'charts': charts,
        'chartPages': PageForCharts.objects.all(),
    }
    return render(request, 'AboutCSharpDeveloper/page_for_charts.html', context)


def show_chart(request, chart_slug):
    context = {
        'chart': Chart.objects.get(slug=chart_slug),
        'chartPages': PageForCharts.objects.all()
    }
    return render(request, 'AboutCSharpDeveloper/chart.html', context)


def recent_vacancies(request):
    vacs = get_c_sharp_vacs(2022, 12, 20).to_dict('records')
    context = {
        'chartPages': PageForCharts.objects.all(),
        'vacs': vacs
    }
    return render(request, 'AboutCSharpDeveloper/recent_vacancies.html', context)
