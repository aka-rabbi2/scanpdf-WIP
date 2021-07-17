from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import timer
from scanpdf.scan_pdf import scan_pdf 
import time


# Create your views here.
def index(request):#
    #timer.timer_func(5, time.time())
    scan_pdf("scanpdf/utils/table.weights")
    return HttpResponseRedirect(reverse("showpdf:index"))
