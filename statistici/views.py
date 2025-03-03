import datetime
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from angajare.models import StatisticaAngajare
from recrutare.models import StatisticaAdaugareCandidati
from .models import Job


class Lista_joburi(ListView):
    model = Job
    template_name = 'statistici/statistici.html'

    def get_queryset(self):
        return Job.objects.order_by('-data')


class ListareJoburiDeAstazi(ListView):
    model = Job
    ordering = ['data']
    template_name = 'statistici/joburi_astazi.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_astazi'] = datetime.date.today()
        return context

    def get_queryset(self):
        return Job.objects.filter(data=datetime.date.today())


class ListaStatistici(ListView):
    model = StatisticaAdaugareCandidati
    template_name = 'statistici/statistica_adaugare_candidati.html'

    def get_queryset(self):
        return StatisticaAdaugareCandidati.objects.order_by('-data_ora')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_candidati_adaugati'] = (
            StatisticaAdaugareCandidati.objects.filter(user=self.request.user).count())
        context['total_angajati_adaugati'] = (
            StatisticaAngajare.objects.filter(user=self.request.user).count())
        context['statistica_adaugare'] = (
            StatisticaAdaugareCandidati.objects.filter(user=self.request.user).order_by('-data_ora'))
        context['statistica_angajare'] = (
            StatisticaAngajare.objects.filter(user=self.request.user).order_by('-data_ora'))
        return context

@csrf_exempt
@login_required
def ruleaza_web_scraping_bestjobs(request):
    if request.method == "POST":
        try:
            call_command('web_scraping')
            return redirect('statistici:lista_joburi_web')
        except Exception as e:
            return redirect('statistici:lista_joburi_web')
    return redirect('statistici:lista_joburi_web')