from django.urls import path

from . import views

app_name = 'userprofile'

urlpatterns = [
    path('new_account/', views.CreateNewAccount.as_view(), name='create_new_account'),
]