from django.urls import path

from . import views
from .views import reziliere_contract, reactivare_contract

app_name = 'angajati'

urlpatterns = [
    path('', views.AdministreazaAngajatii.as_view(), name='administreaza_angajatii'),
    path("<int:pk>/profil_angajat/", views.AngajatDetailView.as_view(), name='profil_angajat'),
    path("update_profil_angajat/<int:pk>/", views.AngajatUpdateView.as_view(), name='update_profil_angajat'),
    path('adauga_angajat/<int:candidat_id>/', views.AdaugaAngajat.as_view(), name='adauga_angajat'),
    path('adauga_angajat/', views.AdaugaAngajat.as_view(), name='adauga_angajat_fara_candidat'),
    path('<int:pk>/reziliere_contract', reziliere_contract, name='reziliere_contract'),
    path('<int:pk>/reactivare_contract', reactivare_contract, name='reactivare_contract'),
    path('<int:angajat_id>/documente_angajati/', views.AdministreazaDocumenteView.as_view(), name='administreaza_documente'),
    path('<int:angajat_id>/documente_angajati/adauga/', views.AdaugaDocumentView.as_view(), name='adauga_document'),
]
