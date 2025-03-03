from django.urls import path

from . import views

app_name = 'statistici'

urlpatterns = [
    path('', views.Lista_joburi.as_view(), name='lista_joburi_web'),
    path('joburi_astazi/', views.ListareJoburiDeAstazi.as_view(), name='joburi_astazi'),
    path('statistici_adaugare/', views.ListaStatistici.as_view(), name='statistici'),
    path('refresh_web_scraping/', views.ruleaza_web_scraping_bestjobs, name='refresh_web_scraping'),
]