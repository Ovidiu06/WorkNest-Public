from django import forms

from recrutare.models import validator_cnp
from .models import Angajat, Document

class AngajatForm(forms.ModelForm):
    este_manager = forms.BooleanField(
        required=False, label='Acest angajat este Manager',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Angajat
        fields = ['nume', 'prenume', 'email', 'telefon', 'cnp', 'tip_act', 'serie_act', 'numar_act', 'data_eliberat_act', 'act_eliberat_de', 'locul_nasterii', 'stare_civila', 'tara', 'judet', 'localitate', 'strada', 'numar_strada', 'bloc', 'scara', 'etaj', 'apartament', 'cv', 'data_angajarii', 'pozitie_angajat']
        widgets = {
            'nume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduceti numele'}),
            'prenume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduceti prenumele'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Introduceti email-ul'}),
            'telefon': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel', 'placeholder': 'Introduceti numarul de telefon'}),
            'cnp': forms.TextInput(
                attrs={'class': 'form-control', 'maxlength': 13, 'placeholder': 'Introduceți CNP-ul'}),
            'data_eliberat_act': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_angajarii': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cv': forms.ClearableFileInput(attrs={'class': 'form-control', 'type': 'file'}),
            'este_manager': forms.CheckboxInput(attrs={'class': 'form-check-input'})}

    def __init__(self, pk=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields.keys():
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })
        self.pk = pk

    def clean(self):
        cnp = self.cleaned_data.get('cnp')
        email = self.cleaned_data.get('email')
        if cnp:
            if not validator_cnp(cnp):
                self.add_error('cnp', 'CNP-ul este gresit! Te rugam sa verifici!')
            else:
                if self.pk:
                    if Angajat.objects.filter(cnp=cnp).exclude(id=self.pk).exists():
                        self.add_error('cnp', f'Exista deja un angajat cu acest CNP! Te rugam sa verifici!')
                    elif Angajat.objects.filter(email=email).exclude(id=self.pk).exists():
                        self.add_error('email',
                                       f'Acest email exista deja in baza de date asociat cu un alt angajat! Te rugam sa verifici!')
                else:
                    if Angajat.objects.filter(cnp=cnp).exists():
                        self.add_error('cnp', f'Exista deja un angajat cu acest CNP! Te rugam sa verifici!')
                    elif Angajat.objects.filter(email=email).exists():
                        self.add_error('email',
                                       f'Acest email exista deja in baza de date asociat cu un alt angajat! Te rugam sa verifici!')
        return self.cleaned_data

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['angajat', 'tip_document', 'document']