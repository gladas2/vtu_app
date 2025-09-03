from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from decimal import Decimal

NETWORK_CHOICES = [
    ('mtn_airtime','MTN Airtime'), ('glo_airtime','Glo Airtime'),
    ('airtel_airtime','Airtel Airtime'), ('9mobile_airtime','9Mobile Airtime'),
    ('mtn_data','MTN Data'), ('glo_data','Glo Data'),
    ('airtel_data','Airtel Data'), ('9mobile_data','9Mobile Data'),
]

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    network = models.CharField(max_length=30, choices=NETWORK_CHOICES)
    amount = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)
    provider_response = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} → {self.network} to {self.phone} for {self.amount}"
    # vtu/models.py



class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def credit(self, amount):
        self.balance += Decimal(amount)
        self.save()

    def debit(self, amount):
        if self.balance >= Decimal(amount):
            self.balance -= Decimal(amount)
            self.save()
            return True
        return False

    def __str__(self):
        return f"{self.user.username}'s Wallet: ₦{self.balance}"


# Create your models here.
# vtu/models.py

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_id = models.CharField(max_length=100, unique=True)
    service = models.CharField(max_length=50)  # e.g. airtime, data, tv
    service_id = models.CharField(max_length=50)  # e.g. 'mtn'
    phone_or_meter = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
