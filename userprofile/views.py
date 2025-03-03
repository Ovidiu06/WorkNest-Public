from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import CreateView
from userprofile.forms import CreateNewAccountForm


class CreateNewAccount(LoginRequiredMixin, CreateView):
    model = User
    template_name = 'registration/adaugare_user.html'
    form_class = CreateNewAccountForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        return redirect('angajati:administreaza_angajatii')