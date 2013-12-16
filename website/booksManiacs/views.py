# Create your views here.

from django.http import HttpResponse
# from django.template import RequestContext, loader

# from booksManiacs.models import Book

def index(request):
    return HttpResponse("Hello, world. The booksManiacs are here.")
