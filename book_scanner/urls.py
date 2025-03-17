from django.urls import path
from . import views

app_name="book_scanner"
urlpatterns=[
    path("", views.BookScannerView.as_view(), name="book_scanner"),
]