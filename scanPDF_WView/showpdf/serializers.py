from rest_framework import serializers 
from .models import PdfTables, BankInfo

class PdfSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PdfTables 
        fields=('date','particulars','instrument','withdraw','deposit','balance')

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankInfo
        fields=('name', 'shorthand', 'company', 'acctype', 'account', 'currency', 'address' )