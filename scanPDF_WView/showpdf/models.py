from django.db import models

# Create your models here.

class BankInfo(models.Model):
    name = models.TextField()
    shorthand = models.CharField(max_length=8)
    company = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    account = models.CharField(max_length=15,blank=True, null=True, unique=True)
    acctype = models.TextField(blank=True, null=True)
    currency = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Bank'
        verbose_name_plural = 'Banks'

class PdfTables(models.Model):

    id = models.AutoField(primary_key=True)
    bank = models.ForeignKey(BankInfo, on_delete = models.CASCADE, related_name="bank_details",blank=True, null=True)
    date = models.DateField()
    particulars = models.TextField(blank=True, null=True)
    instrument = models.TextField(blank=True, null=True)
    withdraw = models.TextField(blank=True, null=True)
    deposit = models.TextField(blank=True, null=True)
    balance = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Statement'
        verbose_name_plural = 'Statements'


