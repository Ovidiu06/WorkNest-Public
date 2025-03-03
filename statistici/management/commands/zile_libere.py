import requests
from django.core.management import BaseCommand
import datetime
from statistici.models import ZileLibere


def zile_libere(*an):
  if an:
    url = f'https://api.bank-holidays.ro/?year={an}'
  else:
    url = f'https://api.bank-holidays.ro/?year={datetime.date.today().year}'

  payload = {}
  headers = {
    'Authorization': 'Token da20bbbb390ba206cc05aa010bd1a2008abc7588'
  }

  response = requests.request("GET", url, headers=headers, data=payload).json()

  for zi_libera in response:
    if ZileLibere.objects.filter(nume=zi_libera['name'], data=zi_libera['date']).exists() is False:
      ZileLibere.objects.create(nume=zi_libera['name'], data=zi_libera['date'])


class Command(BaseCommand):
  help = 'Vizualizare API zile libere'

  def handle(self, *args, **options):
    zile_libere()