from django.db import models
from showpdf.models import BankInfo

# Create your models here.
class Header(models.Model):
    bank_choices = [
        ('sbl', 'standard bank limited'),
        ('bcbl', 'bangladesh commercial bank limited'),
        ('exim', 'Export Import Bank of Bangladesh Limited'),
        ('jbl', "Jamuna Bank Ltd"),
        ('ibbl', 'Islami bank Bangladesh Limited'),
        ('ific', 'international finance investment and commerce bank'),
        ('pbl', 'Pubali bank limited'),
        ('prbl', 'Premier bank limited'),
        ('sbac', 'South bangla agriculture and commerce bank limited'),
        ('sbl', 'standard bank limited'),
        ('sibl', 'Social islami bank limited'),
        ('sjibl', 'Shahjalal islami bank Ltd'),
        ('sobl', 'SOnali bank limited'),
        ('ubl', 'uttara bank limited')

    ]
    bank = models.CharField(max_length=8, choices=bank_choices)
    dates = models.TextField()
    particulars = models.TextField(blank=True, null=True)
    instrument = models.TextField(blank=True, null=True)
    withdraw = models.TextField()
    deposit = models.TextField()
    balance = models.TextField()

    def __str__(self):
        return self.bank

