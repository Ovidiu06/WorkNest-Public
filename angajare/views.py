from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from recrutare.models import Candidat
from .models import Document, Angajat, generator_username,StatisticaAngajare, StatisticaAdaugareDocumente
from .forms import AngajatForm, DocumentForm


class AdministreazaAngajatii(ListView):
    model = Angajat
    template_name = 'angajare/administreaza_angajatii.html'


class AngajatDetailView(LoginRequiredMixin, DetailView):
    model = Angajat
    template_name = 'angajare/profil_angajat.html'


class AngajatUpdateView(LoginRequiredMixin, UpdateView):
    model = Angajat
    form_class = AngajatForm
    template_name = 'angajare/update_profil_angajat.html'

    def form_invalid(self, form):
        print(form.errors)
        return super(AngajatUpdateView, self).form_invalid(form)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        return redirect('angajati:profil_angajat', pk=instance.pk)

    def get_form_kwargs(self):
        data = super().get_form_kwargs()
        if 'pk' in self.kwargs:
            data.update({'pk': self.kwargs['pk']})
        else:
            data.update({'pk': None})
        return data


class AdaugaAngajat(LoginRequiredMixin, CreateView):
    model = Angajat
    form_class = AngajatForm
    template_name = 'angajare/adauga_angajat.html'

    def get_initial(self):
        id_candidat = self.kwargs.get('candidat_id')
        date_formular_angajare = super().get_initial()
        if id_candidat:
            candidat = get_object_or_404(Candidat, id=self.kwargs.get('candidat_id'))
            date_formular_angajare.update({
                'nume': candidat.nume,
                'prenume': candidat.prenume,
                'email': candidat.email,
                'telefon': candidat.numar_telefon,
                'cnp': candidat.CNP,
                'judet': candidat.judet_candidat,
                'localitate': candidat.localitate_candidat,
                'stare_civila': candidat.stare_civila,
                'pozitie_angajat': candidat.pozitie_aplicata,
                'cv': candidat.cv,
                'poza': candidat.poza,
            })
        return date_formular_angajare

    def get_form_kwargs(self):
        data = super().get_form_kwargs()
        data.update({'pk': None})
        return data

    def form_invalid(self, form):
        print(form.errors)
        return super(AdaugaAngajat, self).form_invalid(form)

    def form_valid(self, form):
        email = form.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            form.add_error('email', 'Acest e-mail este deja asociat unui alt utilizator. Te rugam verifica!')
            return self.form_invalid(form)
        user = User.objects.create_user(
            username=generator_username(form.cleaned_data['nume'], form.cleaned_data['prenume']),
            first_name=form.cleaned_data['nume'], last_name=form.cleaned_data['prenume'],
            email=form.cleaned_data['email'],
            password=f'{form.cleaned_data['cnp']}'
        )
        instance = form.save(commit=False)
        instance.user = user
        instance.save()
        instance.este_manager = form.cleaned_data.get('este_manager', False)
        instance.save()
        StatisticaAngajare.objects.create(angajat=instance, user=self.request.user)
        id_candidat = self.kwargs.get('candidat_id')
        if id_candidat:
            candidat = get_object_or_404(Candidat, id=id_candidat)
            candidat.active = False
            candidat.save()
        if form.cleaned_data.get('este_manager'):
            pozitie = form.cleaned_data['pozitie_angajat']
            departament = pozitie.departament
            if not departament.manager_group:
                group_name = f'Manager {departament.nume}'
                group, created = Group.objects.get_or_create(name=group_name)
                departament.manager_group = group
                departament.save()
            user.groups.add(departament.manager_group)
            departament.manager = user
            departament.save()
        pozitie_ocupata = instance.pozitie_angajat
        if pozitie_ocupata:
            pozitie_ocupata.active = False
            pozitie_ocupata.save()
            Candidat.objects.filter(pozitie_aplicata=pozitie_ocupata).update(active=False)
        return redirect('angajati:administreaza_angajatii')


class AdministreazaDocumenteView(LoginRequiredMixin, ListView):
    model = Document
    template_name = 'angajare/administreaza_documente.html'
    context_object_name = 'documente_angajati'

class AdaugaDocumentView(LoginRequiredMixin, CreateView):
    model = Document
    form_class = DocumentForm
    template_name = 'angajare/adauga_document.html'
    success_url = reverse_lazy('angajati:administreaza_documente')

    def form_invalid(self, form):
        print(form.errors)
        return super(AdaugaDocumentView, self).form_invalid(form)

    def form_valid(self, form):
        if form.is_valid() and not form.errors:
            instance = form.save(commit=False)
            instance.save()
            StatisticaAdaugareDocumente.objects.create(angajat=instance.angajat, document=instance.tip_document, user=self.request.user)
            return redirect('angajati:administreaza_angajatii')


@login_required
def reziliere_contract(request, pk):
    Angajat.objects.filter(id=pk).update(active=False)
    return redirect('angajati:administreaza_angajatii')

@login_required
def reactivare_contract(request, pk):
    Angajat.objects.filter(id=pk).update(active=True)
    return redirect('angajati:administreaza_angajatii')