# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
# from django.template import RequestContext, loader

from booksManiacs.models import Book

def home(request):
    return render(request, 'booksManiacs/home.html')

def books(request):
	books_available =  Book.objects.all()                 #books with avail_count!=0
	data = {'books_available': books_available}
	return render(request, 'booksManiacs/books.html', data)
