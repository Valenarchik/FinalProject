from django.contrib import admin
from .models import *


class ChartAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'chart', 'page']
    list_display_links = ['id', 'name']
    prepopulated_fields = {'slug': ('name',)}


class PageForChartsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Chart, ChartAdmin)
admin.site.register(PageForCharts, PageForChartsAdmin)
