from django.contrib import admin
from django.urls import path, include

from AboutCSharpDeveloper.views import *

urlpatterns = [
    path('', index, name='index'),
    path('relevance/', relevance, name='relevance'),
    path('geography/', geography, name='geography'),
    path('skills/', skills, name='skills'),
    path('recent_vacancies/', recent_vacancies, name='recent_vacancies')
]
