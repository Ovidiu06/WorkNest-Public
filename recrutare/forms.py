from django import forms
from django.contrib.auth.models import User

from angajare.models import Angajat
from .models import Candidat, validator_cnp, Pozitie, Departament, Oras, Interviu


class CandidatForm(forms.ModelForm):
    cv = forms.FileField(required=False, label="Incarca CV-ul (Doar fisiere de tip .pdf)")
    class Meta:
        model = Candidat
        fields = [ 'status', 'nume', 'prenume', 'CNP', 'numar_telefon', 'email', 'judet_candidat', 'localitate_candidat', 'stare_civila', 'pozitie_aplicata', 'cv', 'poza']

    def __init__(self, pk, *args, **kwargs):
        super(CandidatForm, self).__init__(*args, **kwargs)
        for field_name in self.fields.keys():
            self.fields[field_name].widget.attrs.update({
                "class": "form-control"
            })
        self.pk = pk

    def clean(self):
        data = self.cleaned_data
        cnp = data.get('CNP')
        email = data.get('email')
        if cnp != None:
            if validator_cnp(cnp) is False:
                msg = "CNP-ul este gresit! Te rugam sa verifici!"
                self._errors['CNP'] = self.error_class([msg])
            else:
                if self.pk:
                    if Candidat.objects.filter(CNP=cnp).exclude(id=self.pk).exists():
                        msg = f"CNP-ul acesta deja exista in baza de date asociat cu un alt candidat! Te rugam sa verifici!"
                        self._errors['CNP'] = self.error_class([msg])
                    elif Candidat.objects.filter(email=email).exclude(id=self.pk).exists():
                        msg = f"Emailul acesta deja exista in baza de date asociat cu un alt candidat! Te rugam sa verifici!"
                        self._errors['email'] = self.error_class([msg])
                else:
                    if Candidat.objects.filter(CNP=cnp).exists():
                        msg = f"CNP-ul acesta deja exista in baza de date asociat cu un alt candidat! Te rugam sa verifici!"
                        self._errors['CNP'] = self.error_class([msg])
                    elif Candidat.objects.filter(email=email).exists():
                        msg = f"Emailul acesta deja exista in baza de date asociat cu un alt candidat! Te rugam sa verifici!"
                        self._errors['email'] = self.error_class([msg])
        return data


class PozitieForm(forms.ModelForm):

    class Meta:
        model = Pozitie
        fields = ['nume', 'departament', 'oras', 'tip_contract', 'mod_de_lucru', 'cod_COR']

    def __init__(self, *args, **kwargs):
        super(PozitieForm, self).__init__(*args, **kwargs)
        for field_name in self.fields.keys():
            self.fields[field_name].widget.attrs.update({
                "class": "form-control"
            })


class DepartamentForm(forms.ModelForm):
    manager = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label="Manager",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Departament
        fields = ['nume', 'manager']
        widgets = {'nume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduceti numele departamentului'}), 'manager': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Selectati Manager'})}
        labels = {'nume': 'Nume Departament', 'manager': 'Manager Departament'}

    def __init__(self, *args, **kwargs):
        departament_id = kwargs.pop('departament_id', None)
        super().__init__(*args, **kwargs)
        if departament_id:
            self.fields['manager'].queryset = User.objects.filter(
                angajat__pozitie_angajat__departament_id=departament_id
            )
        if self.instance and self.instance.manager:
            self.fields['manager'].initial = self.instance.manager.pk

class OrasForm(forms.ModelForm):

    class Meta:
        model = Oras
        fields = ['nume']
        widgets = {'nume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduceti numele orasului'})}
        labels = {'nume': 'Nume Oras'}


class InterviuForm(forms.ModelForm):
    class Meta:
        model = Interviu
        fields = ['data_interviu', 'ora_interviu']
        widgets = {'data_interviu': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), 'ora_interviu': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}), 'manager': forms.Select(attrs={'class': 'form-control'})}
        labels = {'data_interviu': 'Data interviului', 'ora_interviu': 'Ora interviului', 'manager': 'Manager de departament'}