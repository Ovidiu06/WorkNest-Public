from django.urls import path

from recrutare import views

app_name = 'candidati'

urlpatterns = [
    path('', views.CautareCandidati.as_view(), name='recrutare'),
    path('adaugare_candidat_nou/', views.AdaugareCandidatiNoi.as_view(), name='adaugare_candidat_nou'),
    path('adaugare_pozitie_noua/', views.AdaugarePozitieNoua.as_view(), name='adaugare_pozitie_noua'),
    path('adaugare_oras_nou/', views.AdaugareOrasNou.as_view(), name='adaugare_oras_nou'),
    path('<int:pk>/editeaza_oras/', views.EditareOrasView.as_view(), name='editeaza_oras'),
    path('stergere_oras/<int:pk>/', views.stergere_oras, name='stergere_oras'),
    path('adaugare_departament_nou/', views.AdaugareDepartamentNou.as_view(), name='adaugare_departament_nou'),
    path("<int:pk>/profil_candidat/", views.CandidatDetailView.as_view(), name='profil_candidat'),
    path('<int:pk>/update_profil/', views.UpdateCandidatView.as_view(), name='update_profil'),
    path('<int:pk>/stergere_pozitie/', views.stergere_pozitie, name='stergere_pozitie'),
    path('<int:pk>/reactivare_pozitie/', views.reactivare_pozitie, name='reactivare_pozitie'),
    path('pozitii/', views.CautarePozitii.as_view(), name='pozitii_deschise'),
    path('pozitii/<int:pk>/candidati/', views.ListaCandidatiPerPozitie.as_view(), name='lista_candidati_pozitie'),
    path('departamente/', views.ListaDepartamenteView.as_view(), name='lista_departamente'),
    path('departamente/<int:pk>/editeaza/', views.EditareDepartamentView.as_view(), name='editeaza_departament'),
    path('<int:candidat_id>/programeaza_interviu/', views.ProgrameazaInterviu.as_view(), name='programeaza_interviu'),
]