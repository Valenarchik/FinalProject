from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('<slug:page_for_charts_slug>/', show_page_for_chart, name='charts'),
    path('chart/<slug:chart_slug>/', show_chart, name='chart'),
    path('recent_vacancies/', recent_vacancies, name='recent_vacancies')
]
