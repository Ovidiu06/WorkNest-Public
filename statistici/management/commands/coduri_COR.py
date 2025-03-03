import os
import time

import django
from django.core.management import BaseCommand
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WorkNest.settings')
django.setup()

from statistici.models import CoduriCOR


def coduri_COR():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://www.rauflorin.ro/cor-2024-clasificarea-ocupatiilor-din-romania/?')
    driver.find_element(by=By.XPATH, value='//*[@id="cookiescript_accept"]').click()
    driver.find_element(by=By.XPATH, value='//*[@id="table_1_length"]/label/div/button').click()
    driver.find_element(by=By.XPATH, value='//*[@id="table_1_length"]/label/div/div/ul/li[7]/a/span[1]').click()
    scroll_pause_time = 1
    last_height = driver.execute_script('return document.documentElement.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0,document.documentElement.scrollHeight);')
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script('return document.documentElement.scrollHeight')
        if new_height == last_height:
            print('break')
            break
        last_height = new_height
    coduri = []
    for i in range(0, 4532):
        elemente = driver.find_elements(by=By.XPATH, value=f'//*[@id="table_647_row_{0}"]')
        for cod in elemente:
            try:
                cod_cor = cod.find_element(by=By.XPATH, value=f'//*[@id="table_647_row_{i}"]/td[1]').text.lower()
                functia = cod.find_element(by=By.XPATH, value=f'//*[@id="table_647_row_{i}"]/td[2]').text.lower()
                coduri.append({'cod_cor': cod_cor, 'functia': functia})
            except Exception:
                cod_cor = False
                functia = False

    driver.quit()
    for cod in coduri:
        if CoduriCOR.objects.filter(cod=cod['cod_cor'], functia=cod['functia']).exists() is False:
            CoduriCOR.objects.create(cod=cod['cod_cor'], functia=cod['functia'])


class Command(BaseCommand):
  help = 'Vizualizare API zile libere'

  def handle(self, *args, **options):
    coduri_COR()