from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Departament

@receiver(post_save, sender=Departament)
def create_manager_group(sender, instance, created, **kwargs):
    if created and not instance.manager_group:
        group = Group.objects.create(name=f'Manager {instance.nume}')
        instance.manager_group = group
        instance.save()
        print(f'Am creat grupul: Manager {instance.nume}')