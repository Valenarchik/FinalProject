from django.db import models
from django.urls import reverse


class Chart(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название графика')
    slug = models.SlugField(max_length=99, unique=True, db_index=True, verbose_name='URL')
    chart = models.ImageField(upload_to='charts', verbose_name='График')
    table = models.TextField(blank=True, verbose_name='Таблица')
    page = models.ForeignKey('PageForCharts', on_delete=models.PROTECT, verbose_name="Страница")

    def get_absolute_url(self):
        return reverse('chart', kwargs={'chart_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "график"
        verbose_name_plural = "графики"


class PageForCharts(models.Model):
    name = models.CharField(max_length=99, verbose_name='Название страницы')
    slug = models.SlugField(max_length=99, unique=True, db_index=True, verbose_name='URL')

    def get_absolute_url(self):
        return reverse('charts', kwargs={'page_for_charts_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "страницу c графиками"
        verbose_name_plural = "страницы с графиками"
