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

from statistici.models import Job

def web_scraping():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://www.bestjobs.eu/locuri-de-munca/brasov/recent')
    driver.find_element(by=By.XPATH, value='//*[@id="headlessui-dialog-panel-:rf:"]/div/button[2]').click()
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
    driver.find_element(by=By.XPATH, value='// *[ @ id = "__next"] / div / div[2] / div[5] / button').click()
    scroll_pause_time = 1
    last_height = driver.execute_script('return document.documentElement.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0,document.documentElement.scrollHeight);')
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script('return document.documentElement.scrollHeight')
        if new_height == last_height:
            print("break")
            break
        last_height = new_height
    driver.find_element(by=By.XPATH, value='// *[ @ id = "__next"] / div / div[2] / div[5] / button').click()
    while True:
        driver.execute_script('window.scrollTo(0,document.documentElement.scrollHeight);')
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script('return document.documentElement.scrollHeight')
        if new_height == last_height:
            print('break')
            break
        last_height = new_height
    driver.find_element(by=By.XPATH, value='// *[ @ id = "__next"] / div / div[2] / div[5] / button').click()
    while True:
        driver.execute_script('window.scrollTo(0,document.documentElement.scrollHeight);')
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script('return document.documentElement.scrollHeight')
        if new_height == last_height:
            print('break')
            break
        last_height = new_height
    joburi = []
    for i in range(2, 150):
        job_elements = driver.find_elements(by=By.XPATH, value=f'//*[@id="__next"]/div[1]/div[2]/div[3]/div[{i}]')

        for job in job_elements:
            try:
                titlu_job = job.find_element(by=By.XPATH, value=f"//*[@id='__next']/div[1]/div[2]/div[3]/div[{i}]/div[1]/h2").text.lower()
                companie = job.find_element(by=By.XPATH, value=f"//*[@id='__next']/div[1]/div[2]/div[3]/div[{i}]/div[1]/div[2]").text.lower()
                link = job.find_element(by=By.XPATH, value=f"//*[@id='__next']/div[1]/div[2]/div[3]/div[{i}]/a").get_attribute("href")
                joburi.append({"titlu_job": titlu_job, "companie": companie, "link": link})
            except Exception:
                titlu_job = False
                companie = False
                link = False
    driver.quit()
    for job in joburi:
        if Job.objects.filter(titlu_job=job['titlu_job'], companie=job['companie'], link=job['link'], platforma='BestJobs.ro').exists() is False:
            Job.objects.create(titlu_job=job['titlu_job'], companie=job['companie'], link=job['link'], platforma='BestJobs.ro')


class Command(BaseCommand):
    help = 'Web Scraping pe BestJobs'

    def handle(self, *args, **options):
        web_scraping()
