from django.shortcuts import render
from django.http import HttpResponse
from headers_temp.scan_headers import scan_headers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
# from scanpdf.scan_pdf import scan_pdf 

# Create your views here.
@api_view(['GET'])
def headers(request):
    scan_headers("headers_temp/utils/headers.weights", "headers_temp/utils/bank.weights")
    # scan_pdf()
    # print(re.search(pattern, headers_list))
    return Response(status = status.HTTP_200_OK)