from django.db import models
from django.contrib.auth.models import User


# Model to store user profile and balance
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)  # User's balance

    def __str__(self):
        return f"{self.user.username}'s Profile"


# Model to store cryptocurrency transactions
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto_name = models.CharField(max_length=10)  # e.g., BTC, ETH, SOL
    amount = models.DecimalField(max_digits=10, decimal_places=4)  # Amount of crypto bought/sold
    transaction_type = models.CharField(max_length=10)  # 'buy' or 'sell'
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of transaction

    def __str__(self):
        return f"{self.user.username} {self.transaction_type} {self.amount} {self.crypto_name}"


# Automatically create a UserProfile when a new user is created
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Automatically save the UserProfile when the User is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
