from django.db import models


class Job(models.Model):
    titlu_job = models.CharField(max_length=255)
    companie = models.CharField(max_length=255)
    link = models.URLField()
    platforma = models.CharField(max_length=50, null=True, blank=True)
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.titlu_job


class ZileLibere(models.Model):
    nume = models.CharField(max_length=255)
    data = models.DateField(unique=True)

    def __str__(self):
        return f'{self.data:%d-%m-%Y}'


class CoduriCOR(models.Model):
    cod = models.CharField(max_length=10, null=True, blank=True)
    functia = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f'{self.cod} - {self.functia}'
