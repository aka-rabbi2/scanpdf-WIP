from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework import serializers
from rest_framework.serializers import Serializer
from showpdf.models import PdfTables, BankInfo
from .serializers import PdfSerializer, BankSerializer
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage

# Create your views here.
def pagination_helper(page,total):
    if total <= 3:
        return (1, 2, 3)
    elif total-page<page:
        return (1, 2, '...', total-3, total-2, total-1, total)
    elif total-page==page:
        return (page, page+1, page+2, total-2, total-1, total)
    else:
        return (page, page+1, page+2, '...',total-2, total-1, total)

def index(request, page=1, post_range=10):
    # page = int(request.GET.get('p', '1'))
    page = int(page)
    table_rows = PdfTables.objects.all().order_by('date')
    paginator = Paginator(table_rows, post_range)
    total_pages = paginator.num_pages
    pages_list = pagination_helper(page, total_pages)

    try:
        paginated_rows = paginator.page(page)
    except ValueError:
        paginated_rows = paginator.page(1)
    except EmptyPage:
        paginated_rows = paginator.page(paginator.num_pages)   
    return render(request, "showpdf/index.html", {
        "rows": paginated_rows,
        "total": pages_list
    })

def bank_details(request, data_id):
    bank = PdfTables.objects.get(id=data_id).bank
    return render(request, "showpdf/bank.html",{
        "bank":bank,
    })

def edit_bank(request, data_id):
    try:
        row = PdfTables.objects.get(id=data_id)
        bank = row.bank
    except PdfTables.DoesNotExist:
        print(data_id,'post')

    # serializer = PdfSerializer(row)

    if request.method=='GET':
        return render(request, "showpdf/edit.html", {
            "data":row,
            "date":str(row.date),
            "bank":bank
        })
    elif request.method == "POST":
        print("........................................")
        #print(request.data.get("particulars"))
        data = {
            "date": request.POST.get("Date"),
            "particulars": request.POST.get("Particulars"),
            "instrument": request.POST.get("Instrument"),
            "withdraw": request.POST.get("Withdraw"),
            "deposit": request.POST.get("Deposit"),
            "balance": request.POST.get("Balance"),
        }
        print(data)
        bank_data = {
            'name': request.POST.get("Name"),
            'shorthand': request.POST.get("Shorthand"),
            'company': request.POST.get("Company"),
            'acctype': request.POST.get("Type"),
            'account': request.POST.get("Account"),
            'currency': request.POST.get("Currency"),
            'address': request.POST.get("Address")
        }

        serializer = PdfSerializer(row, data=data)
        bank_serializer = BankSerializer(bank, data=bank_data)

        if serializer.is_valid() and bank_serializer.is_valid():
            serializer.save()
            bank_serializer.save()
            return HttpResponseRedirect(reverse("showpdf:index"))
        elif serializer.is_valid():
            serializer.save()
            return HttpResponseRedirect(reverse("showpdf:index"))
        elif bank_serializer.is_valid():
            bank_serializer.save()
            return HttpResponseRedirect(reverse("showpdf:index"))
        
        else:
            return render(request, "showpdf/edit.html", {
            "data":row,
            "error":serializer.errors
        })
    # else:
        
    #     data = PdfTables.objects.get(id=data_id)
    #     print(type(data.withdraw),data.deposit,data.balance)
    #     return render(request, "showpdf/edit.html", {
    #         "data":data,
    #         "date":str(data.date)
    #     })

@api_view(['PUT'])
def edit_statement(request):
    row = PdfTables.objects.get(id=request.data.get('pk'))

    if request.method == "PUT":
        header = request.data.get('column').lower()
        datapoint = request.data.get('datapoint')
        serializer = PdfSerializer(row, data={header: datapoint, 'date': row.date})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)