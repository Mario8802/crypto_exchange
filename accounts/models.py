from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)  

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto_name = models.CharField(max_length=10) 
    amount = models.DecimalField(max_digits=10, decimal_places=4)  
    transaction_type = models.CharField(max_length=10)  
    timestamp = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.user.username} {self.transaction_type} {self.amount} {self.crypto_name}"



from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
