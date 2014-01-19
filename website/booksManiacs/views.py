# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
# from django.template import RequestContext, loader

from booksManiacs.models import Book, Item, Profile

def home(request):
	if request.session.get('user'):
		name = request.session.get('user')
		return render(request, 'booksManiacs/home.html', {'name': name})
	else:
		return render(request, 'booksManiacs/home.html')

def books(request):
	books_available =  Book.objects.all()                 # books with avail_count!=0
	data = {'books_available': books_available}
	return render(request, 'booksManiacs/books.html', data)

def items(request, book_author):
	exist = Book.objects.filter(author=book_author).count()
	if exist:
		# return HttpResponse("<h1>It works! %s</h1>" % book_author)
		req_items = Item.objects.filter(name=book_author)
		data = {'req_items' : req_items, 'book_author' : book_author, 'exist' : exist}
		return render(request, 'booksManiacs/items.html', data)
	else:
		return HttpResponse("sorry there is no such book. you have reached the wrong page.")
		#404page

def login(request):
	if 'user' in request.session:
		name = request.session['user']
		return HttpResponseRedirect("/booksManiacs/")

	else:
		if 'user' in request.POST:
			email = request.POST['user']
			userExist = Profile.objects.filter(email=email).count()
			if userExist:
				loginPassword = request.POST['password']
				realPassword = Profile.objects.get(email=email).password
				print realPassword
				if loginPassword == realPassword:
					request.session['user'] = email
					return HttpResponseRedirect("/booksManiacs/")
				else:
					data = {'errorString': 'your username and password didnt match'}
					return render(request, 'booksManiacs/login.html', data)
			else:
				return HttpResponse("this id is not registered on our site")
		else:
			return render(request, 'booksManiacs/login.html')


def logout(request):
	if 'user' in request.session:
		del request.session['user']
		return HttpResponseRedirect("/booksManiacs/")
	else:
		return HttpResponse("You have been successfull in finding a broken link..well you are lost")

def signup(request):
	if 'name' in request.POST:
		name        = request.POST['name']
		email       = request.POST['email']
		phone       = request.POST['phone']
		password    = request.POST['pass']
		confirmPass = request.POST['confPass']
		bhawan      = request.POST['bhawan']
		room        = request.POST['room']
		enrNo       = request.POST['enrNo']
		year        = request.POST['year']
		p = Profile.objects.create(name = name, email = email, password = password, mobile_number = phone, room_number = room, hostel = "clb", year = year, enrollment_number = enrNo)
		return HttpResponse("yeah here")
	else:
		return HttpResponseRedirect("/booksManiacs/")