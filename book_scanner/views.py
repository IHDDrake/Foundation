from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class BookScannerView(TemplateView):
    template_name = "book_scanner.html"
