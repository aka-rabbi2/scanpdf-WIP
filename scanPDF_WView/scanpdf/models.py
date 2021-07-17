from django.db import models

# Create your models here.

class PdfHeader(models.Model):
    pdf_name = models.CharField(primary_key=True, max_length=20)
    dates_index = models.IntegerField(default=-2021)
    particulars_index = models.IntegerField(default=-2021)
    instrument_index = models.IntegerField(default=-2021)
    withdraw_index = models.IntegerField(default=-2021)
    deposit_index = models.IntegerField(default=-2021)
    balance_index = models.IntegerField(default=-2021)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_index(self, header, index):
        return self.date_index
    
    class Meta:
        ordering = ('-created_at',)