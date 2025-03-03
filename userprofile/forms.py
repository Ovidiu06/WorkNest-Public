from django import forms
from django.contrib.auth.models import User
from django.forms import TextInput


class CreateNewAccountForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        widgets = {'first_name': TextInput(attrs={'placeholder': 'Nume', 'class': 'form-control'}),
            'last_name': TextInput(attrs={'placeholder': 'Prenume', 'class': 'form-control'}),
            'Email': TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'username': TextInput(attrs={'placeholder': 'Nume utilizator', 'class': 'form-control'})}

    def clean(self):
        data = self.cleaned_data
        email_value = data.get('email')
        username_value = data.get('username')
        if User.objects.filter(email=email_value).exists():
            msg = 'Emailul acesta deja exista! Te rugam sa furniezi un alt email!'
            self._errors['email'] = self.error_class([msg])
        elif User.objects.filter(username=username_value).exists():
            msg = 'Username-ul acesta deja exista! Te rugam sa furniezi un alt username!'
            self._errors['username'] = self.error_class([msg])
        return data

class ResetPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Introdu adresa de email'}))
    new_password1 = forms.CharField(label='Parola noua', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parola noua'}))
    new_password2 = forms.CharField(label='Confirmare parola', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmare parolă'}))