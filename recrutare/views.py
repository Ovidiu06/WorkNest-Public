from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from angajare.models import Angajat
from recrutare.models import Candidat, Pozitie, Oras, Departament, Interviu
from django.urls import reverse, reverse_lazy
from .forms import CandidatForm, PozitieForm, DepartamentForm, OrasForm, InterviuForm
from .models import StatisticaAdaugareCandidati


class CautareCandidati(LoginRequiredMixin, ListView):
    model = Candidat
    template_name = 'recrutare/lista_candidati.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return Candidat.objects.filter(active=True)

class CandidatDetailView(LoginRequiredMixin, DetailView):
    model = Candidat
    template_name = 'recrutare/profil_candidat.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        toti_candidatii = list(Candidat.objects.filter(pozitie_aplicata=self.object.pozitie_aplicata, active=True).order_by('id'))
        index_curent = [cand.id for cand in toti_candidatii].index(self.object.id)

        if index_curent > 0:
            index_anterior = toti_candidatii[index_curent - 1].id
            context['url_anterior'] = reverse_lazy('candidati:profil_candidat', args=[index_anterior])

        if index_curent < len(toti_candidatii) - 1:
            index_urmator = toti_candidatii[index_curent + 1].id
            context['url_urmator'] = reverse_lazy('candidati:profil_candidat', args=[index_urmator])

        return context

class AdaugareCandidatiNoi(LoginRequiredMixin, CreateView):
    model = Candidat
    form_class = CandidatForm
    template_name = 'recrutare/adaugare_candidat_nou.html'

    def form_invalid(self, form):
        print(form.errors)
        return super(AdaugareCandidatiNoi, self).form_invalid(form)

    def form_valid(self, form):
        if form.is_valid() and not form.errors:
            email = form.cleaned_data['email']
            if Angajat.objects.filter(email=email).exists():
                form.add_error('email', 'Acest e-mail este deja asociat unui alt utilizator. Te rugam verifica!')
                return self.form_invalid(form)
            instance = form.save(commit=False)
            instance.save()
            StatisticaAdaugareCandidati.objects.create(candidat=instance, user=self.request.user)
            return redirect('candidati:recrutare')

    def get_form_kwargs(self):
        data = super().get_form_kwargs()
        data.update({'pk': None})
        return data


class UpdateCandidatView(LoginRequiredMixin, UpdateView):
    model = Candidat
    form_class = CandidatForm
    template_name = 'recrutare/profil_candidat_update.html'

    def form_invalid(self, form):
        print(form.errors)
        return super(UpdateCandidatView, self).form_invalid(form)

    def form_valid(self, form):
        if form.is_valid() and not form.errors:
            instance = form.save(commit=False)
            if 'cv' in self.request.FILES:
                fisier_cv = self.request.FILES['cv']
                nume_cv = f"{instance.pk}_cv.{fisier_cv.name.split('.')[-1]}"
                instance.cv.save(nume_cv, fisier_cv)
            if 'poza' in self.request.FILES:
                photo_file = self.request.FILES['poza']
                nume_poza = f"{instance.pk}_poza_profil.{photo_file.name.split('.')[-1]}"
                instance.poza.save(nume_poza, photo_file)
            instance.save()

            print(self.request.FILES)
            return redirect('candidati:recrutare')

    def get_form_kwargs(self):
        data = super().get_form_kwargs()
        if 'pk' in self.kwargs:
            data.update({'pk': self.kwargs['pk']})
        else:
            data.update({'pk': None})
        return data


class AdaugareOrasNou(LoginRequiredMixin, CreateView):
    model = Oras
    fields = '__all__'
    template_name = 'recrutare/adaugare_oras_nou.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orase'] = list(Oras.objects.values('id', 'nume'))
        return context

    def get_success_url(self):
        return reverse('candidati:recrutare')


class AdaugareDepartamentNou(LoginRequiredMixin, CreateView):
    model = Departament
    form_class = DepartamentForm
    template_name = 'recrutare/adaugare_departament_nou.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departamente'] = Departament.objects.all()
        return context

    def get_success_url(self):
        return reverse('candidati:recrutare')


class AdaugarePozitieNoua(LoginRequiredMixin, CreateView):
    model = Pozitie
    form_class = PozitieForm
    template_name = 'recrutare/adaugare_pozitie_noua.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pozitii'] = Pozitie.objects.all()
        return context

    def get_success_url(self):
        return reverse('candidati:pozitii_deschise')


class CautarePozitii(LoginRequiredMixin, ListView):
    model = Pozitie
    template_name = 'recrutare/lista_pozitii.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get('sort', 'id')
        order = self.request.GET.get('order', 'asc')
        if sort_by in ['id', 'nume', 'departament__nume', 'oras']:
            if order == 'desc':
                sort_by = f'-{sort_by}'
            queryset = queryset.order_by(sort_by)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pozitii'] = Pozitie.objects.filter(active=True)
        pozitie_candidati = (
            Candidat.objects.filter(active=True)
            .values('pozitie_aplicata')
            .annotate(numar_candidati=Count('id'))
        )
        numar_candidati_per_pozitie = {
            item['pozitie_aplicata']: item['numar_candidati']
            for item in pozitie_candidati
        }

        context['numar_candidati_per_pozitie'] = numar_candidati_per_pozitie
        return context

def stergere_pozitie(request, pk):
    if request.user.is_superuser:
        Pozitie.objects.filter(id=pk).update(active=False)
        return redirect('candidati:pozitii_deschise')
    else:
        return redirect('candidati:pozitii_deschise')

def reactivare_pozitie(request, pk):
    if request.user.is_superuser:
        Pozitie.objects.filter(id=pk).update(active=True)
        return redirect('candidati:pozitii_deschise')
    else:
        return redirect('candidati:pozitii_deschise')


class ListaCandidatiPerPozitie(LoginRequiredMixin, ListView):
    model = Candidat
    template_name = 'recrutare/lista_candidati_pozitie.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        id_pozitie = Pozitie.objects.get(pk=self.kwargs['pk']).pk
        queryset = Candidat.objects.filter(pozitie_aplicata=id_pozitie, active=True)
        sort_by = self.request.GET.get('sort', 'id')
        order = self.request.GET.get('order', 'asc')
        if sort_by in ['id', 'nume', 'data_aplicarii', 'status', 'varsta']:
            if order == 'desc':
                sort_by = f'-{sort_by}'
            queryset = queryset.order_by(sort_by)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pozitie = get_object_or_404(Pozitie, pk=self.kwargs['pk'])
        context['numar_candidati'] = len(list(Candidat.objects.filter(pozitie_aplicata=pozitie, active=True)))
        context['pozitie'] = pozitie.nume
        context['oras'] = pozitie.oras
        return context


class ListaDepartamenteView(LoginRequiredMixin, ListView):
    model = Departament
    template_name = 'recrutare/lista_departamente.html'
    context_object_name = 'departamente'


class EditareDepartamentView(LoginRequiredMixin, UpdateView):
    model = Departament
    form_class = DepartamentForm
    template_name = 'recrutare/departament_update.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['departament_id'] = self.object.id
        return kwargs

    def form_invalid(self, form):
        print('Submitted manager value:', self.request.POST.get('manager'))
        print('Form errors:', form.errors)
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('candidati:lista_departamente')

    def form_valid(self, form):
        nou_manager = form.cleaned_data.get('manager')
        grup_manager = self.object.manager_group
        angajati_departament = Angajat.objects.filter(pozitie_angajat__departament=self.object)
        for angajat in angajati_departament:
            if angajat.este_manager:
                if grup_manager and angajat.user.groups.filter(id=grup_manager.id).exists():
                    angajat.user.groups.remove(grup_manager)
                angajat.este_manager = False
                angajat.save()
        if nou_manager:
            angajat_manager = Angajat.objects.get(user=nou_manager)
            angajat_manager.este_manager = True
            angajat_manager.save()
            if grup_manager:
                nou_manager.groups.add(grup_manager)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('candidati:lista_departamente')


class EditareOrasView(LoginRequiredMixin, UpdateView):
    model = Oras
    form_class = OrasForm
    template_name = 'recrutare/oras_update.html'

    def get_success_url(self):
        return reverse('candidati:adaugare_oras_nou')


class ProgrameazaInterviu(CreateView):
    model = Interviu
    form_class = InterviuForm
    template_name = 'recrutare/programeaza_interviu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        candidat_id = self.kwargs.get('candidat_id')
        context['candidat'] = get_object_or_404(Candidat, id=candidat_id)
        return context

    def form_invalid(self, form):
        print(form.errors)
        return super(ProgrameazaInterviu, self).form_invalid(form)

    def form_valid(self, form):
        candidat_id = self.kwargs['candidat_id']
        print(f'Candidat ID: {candidat_id}')
        candidat = Candidat.objects.get(id=candidat_id)
        form.instance.candidat = candidat
        departament = candidat.pozitie_aplicata.departament
        group_name = f'Manager {departament.nume}'
        manager_group = Group.objects.filter(name=group_name).first()
        if manager_group:
            manager = User.objects.filter(groups=manager_group).first()
            if manager:
                form.instance.manager = manager
            else:
                form.add_error(None, f'Nu putem programa interviul. Nu exista setat {group_name}.')
                return self.form_invalid(form)
        else:
            form.add_error(None, f'Grupul {group_name} nu exista.')
            return self.form_invalid(form)
        response = super().form_valid(form)
        send_mail(
            subject=f'Interviu programat cu {candidat.nume} {candidat.prenume}',
            message=f'Interviul este programat pe {form.instance.data_interviu} la ora {form.instance.ora_interviu}. Detalii despre candidat: http://127.0.0.1:8000/recrutare/{candidat.id}/profil_candidat/',
            from_email='noreply@example.com',
            recipient_list=[form.instance.manager.email],
            fail_silently=False,
        )
        return response

    def get_success_url(self):
        return reverse('candidati:recrutare')

def stergere_oras(request, pk):
    if request.user.is_superuser:
        if request.method == 'POST':
            oras = get_object_or_404(Oras, pk=pk)
            oras.delete()
            messages.success(request, f'Orasul "{oras.nume}" a fost sters cu succes.')
        return redirect('candidati:adaugare_oras_nou')