from django.contrib.auth.models import User
from .models import Customer
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def post_save_create_customer (sender, instance, created, *args, **Kwargs):
    if created:
        Customer.objects.create(user=instance)

