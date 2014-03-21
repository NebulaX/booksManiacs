# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
# from django.template import RequestContext, loader

from booksManiacs.models import Book, Item, Profile
from recaptcha.client import captcha

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
		if request.session.get('user'):
			name = request.session.get('user')
			req_items = Item.objects.filter(name=book_author, buy_request=0).exclude(seller=name)
			own_items = Item.objects.filter(name=book_author, seller=name).count()
			data = {'req_items' : req_items, 'book_author' : book_author, 'exist' : exist, 'name' : name, 'own_items' : own_items}
		else:
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
		return HttpResponse('You have been successfull in finding a broken link..well you are lost<br /><a href="/booksManiacs/">home</a>')

def signup(request):
	if 'user' in request.session:
		return HttpResponseRedirect("/booksManiacs/")
	else:
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
			# other checks
			if password == confirmPass:
				response = captcha.submit(  
					request.POST.get('recaptcha_challenge_field'),
					request.POST.get('recaptcha_response_field'),
					'6Le7XvASAAAAAKk5cQcHOwxBRNjKBl49I_yRw2ym',
					request.META['REMOTE_ADDR'],)
				if response.is_valid:
					p = Profile.objects.create(name = name, email = email, password = password, mobile_number = phone, room_number = room, hostel = bhawan, year = year, enrollment_number = enrNo)
					messageString = "you have registered successfully"
					return render(request, 'booksManiacs/login.html', {'messageString': messageString})
				else:
					errorString = 'please fill the captcha correctly'
					return render(request, 'booksManiacs/signup.html', {'errorString': errorString})
			else:
				errorString = "your password did not match with the confirm password"
				return render(request, 'booksManiacs/signup.html', {'errorString': errorString})
		else:
			return render(request, 'booksManiacs/signup.html')

def buy(request,bookId):
	if request.session.get('user'):
		buyer = request.session.get('user')
		exist = Item.objects.filter(pk=bookId).count()
		if exist:
			p = Item.objects.get(pk=bookId)
			ibuyer = Profile.objects.get(email=buyer)
			p.buyer = ibuyer
			p.buy_request = 1
			p.save()
			messageString = "Your request has been registered. We would be contacting you soon for the transaction."
			return HttpResponseRedirect("/booksManiacs/", {'messageString': messageString})
		else:
			return HttpResponseRedirect("/booksManiacs/")
	else:
		return HttpResponseRedirect("/booksManiacs/")
	# return render(request, 'booksManiacs/buy.html')

def sell(request):
	if 'author' in request.POST:
		author    = request.POST['author']
		edition   = request.POST['edition']
		other     = request.POST['other']
		# other checks
		if author == "--------":
			errorString = "plz fill in a valid author"
			allBooks = Book.objects.order_by('author')
			return render(request, 'booksManiacs/sell.html', {'allBooks': allBooks, 'errorString': errorString})
		else:
			b = Book.objects.get(author=author)
			seller = request.session.get('user')
			p = Profile.objects.get(email=seller)
			i = Item.objects.create(name = b, edition = edition, seller = p, other_details = other)
			b.avail_count += 1
			b.save()
			return HttpResponseRedirect("/booksManiacs/")
	else:
		allBooks = Book.objects.order_by('author')
		return render(request, 'booksManiacs/sell.html', {'allBooks': allBooks})

def profile(request):
	if request.session.get('user'):
		name = request.session['user']
		print name
		sellerOf = Item.objects.filter(seller = name)
		buyerOf = Item.objects.filter(buyer = name)
		data = {'sellerOf' : sellerOf,'buyerOf' : buyerOf, 'name' : name}
		return render(request, 'booksManiacs/profile.html', data)
	else:
		return HttpResponseRedirect("/booksManiacs/login/")

def password(request):
	if request.session.get('user'):
		email = request.session['user']
		if 'oldPass' in request.POST:
			oldPass    = request.POST['oldPass']
			newPass    = request.POST['newPass']
			confPass   = request.POST['confPass']
			if newPass != confPass:
				return HttpResponse("the two passwords you entered did not match.")
			user = Profile.objects.get(email=email)
			realPassword = user.password
			if oldPass == realPassword:
				user.password = newPass
				user.save()
				return HttpResponseRedirect("/booksManiacs/profile")
			else:
				return HttpResponse("entered wrong password")
		else:
			return render(request, 'booksManiacs/password.html')
	else:
		return HttpResponseRedirect("/booksManiacs/")