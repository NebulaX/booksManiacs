# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
# from django.template import RequestContext, loader
from django.core.mail import send_mail, EmailMultiAlternatives
import string
import random

from bookManiacs.models import Book, Item, Profile
from recaptcha.client import captcha

def home(request):
	if request.session.get('user'):
		name = request.session.get('user')
		return render(request, 'bookManiacs/home.html', {'name': name})
	else:
		return render(request, 'bookManiacs/home.html')

def books(request):
	books_available =  Book.objects.all()                 # books with avail_count!=0
	data = {'books_available': books_available}
	return render(request, 'bookManiacs/books.html', data)

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
		return render(request, 'bookManiacs/items.html', data)
	else:
		return HttpResponse('sorry there is no such book. you have reached the wrong page.<br /><a href="/booksManiacs/">home</a>')
		#404page

def login(request):
	if 'user' in request.session:
		name = request.session['user']
		return HttpResponseRedirect("/bookManiacs/")
	else:
		if 'user' in request.POST:
			email     = request.POST['user']
			userExist = Profile.objects.filter(email=email).exists()
			if userExist:
				user          = Profile.objects.get(email=email)
				userName      = user.name
				userPassword  = user.password
				userEmail     = user.email
				loginPassword = request.POST['password']
				if loginPassword == userPassword:
					request.session['user'] = userEmail
					request.session['name'] = userName
					return HttpResponseRedirect("/bookManiacs/")
				else:
					data = {'errorString': 'your username and password didnt match'}
					return render(request, 'bookManiacs/login.html', data)
			else:
				data = {'errorString': 'This id is not registered. Maybe you wanna <a href="/bookManiacs/signup/">signup</a>'}
				return render(request, 'bookManiacs/login.html', data)
		else:
			# sendEmail()
			return render(request, 'bookManiacs/login.html')

def logout(request):
	if 'user' in request.session:
		del request.session['user']
		return HttpResponseRedirect("/bookManiacs/")
	else:
		return HttpResponse('You have been successfull in finding a broken link..well you are lost<br /><a href="/bookManiacs/">home</a>')

def signup(request):
	if 'user' in request.session:
		return HttpResponseRedirect("/bookManiacs/")
	else:
		if 'name' in request.POST:
			name        = request.POST['name']
			email       = request.POST['email']
			phone       = request.POST['phone']
			password    = request.POST['pass']
			confirmPass = request.POST['confPass']
			bhawan      = request.POST['bhawan']
			room        = request.POST['room']
			# enrNo       = request.POST['enrNo']
			# year        = request.POST['year']
			# if makeValidation():
			if password == confirmPass:
				response = captcha.submit(
					request.POST.get('recaptcha_challenge_field'),
					request.POST.get('recaptcha_response_field'),
					'6Le7XvASAAAAAKk5cQcHOwxBRNjKBl49I_yRw2ym',
					request.META['REMOTE_ADDR'],)
				if response.is_valid:
					p = Profile.objects.create(name = name, email = email, password = password, mobile_number = phone, room_number = room, hostel = bhawan)

					messageString = 'you have registered successfully'
					return render(request, 'bookManiacs/login.html', {'messageString': messageString})
				else:
					errorString = 'please fill the captcha correctly'
					return render(request, 'bookManiacs/signup.html', {'errorString': errorString})
			else:
				errorString = 'your password did not match with the confirm password'
				return render(request, 'bookManiacs/signup.html', {'errorString': errorString})
		else:
			return render(request, 'bookManiacs/signup.html')

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
			return HttpResponseRedirect("/bookManiacs/", {'messageString': messageString})
		else:
			return HttpResponseRedirect('/bookManiacs/')
	else:
		return HttpResponseRedirect('/bookManiacs/')
	# return render(request, 'bookManiacs/buy.html')

def sell(request):
	if request.session.get('user'):
		if 'author' in request.POST:
			author    = request.POST['author']
			edition   = request.POST['edition']
			other     = request.POST['other']
			# other checks
			if author == "--------":
				errorString = "plz fill in a valid author"
				allBooks = Book.objects.order_by('author')
				return render(request, 'bookManiacs/sell.html', {'allBooks': allBooks, 'errorString': errorString})
			else:
				b = Book.objects.get(author=author)
				print author
				seller = request.session.get('user')
				print seller
				p = Profile.objects.get(email=seller)
				i = Item.objects.create(name = b, edition = edition, seller = p, other_details = other)
				b.avail_count += 1
				b.save()
				return HttpResponseRedirect("/bookManiacs/sell/")
		else:
			allBooks = Book.objects.values_list('author', flat=True).order_by('author')
			authorsList = []
			for book in allBooks:
				authorsList.append(str(book))
				# book = unicodedata.normalize('NFKD', book).encode('ascii','ignore')
			print authorsList
			return render(request, 'bookManiacs/sell.html', {'allBooks': authorsList})
	else:
		return HttpResponseRedirect('/bookManiacs/')

def profile(request):
	if request.session.get('user'):
		name = request.session['user']
		print name
		sellerOf = Item.objects.filter(seller = name)
		buyerOf = Item.objects.filter(buyer = name)
		data = {'sellerOf' : sellerOf,'buyerOf' : buyerOf, 'name' : name}
		return render(request, 'bookManiacs/profile.html', data)
	else:
		return HttpResponseRedirect("/bookManiacs/login/")

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
				return HttpResponseRedirect("/bookManiacs/profile")
			else:
				return HttpResponse("entered wrong password")
		else:
			return render(request, 'bookManiacs/password.html')
	else:
		return HttpResponseRedirect("/bookManiacs/")

def removeBuy(request, bookId):
	if request.session.get('user'):
		buyer = request.session.get('user')
		exist = Item.objects.filter(pk=bookId).count()
		if exist:
			p = Item.objects.get(pk=bookId)
			p.buyer = None
			p.buy_request = 0
			p.save()
			messageString = "The book has been removed from your buy list"
			return HttpResponseRedirect("/bookManiacs/profile/", {'messageString': messageString})
		else:
			return HttpResponseRedirect("/bookManiacs/profile/")
	else:
		return HttpResponseRedirect("/bookManiacs/login/")

def removeBook(request, bookId):
	if request.session.get('user'):
		seller = request.session.get('user')
		exist = Item.objects.filter(pk=bookId).count()
		if exist:
			p = Item.objects.get(pk=bookId)
			p.delete()
			messageString = "The book has been removed from your sell items"
			return HttpResponseRedirect("/bookManiacs/profile/", {'messageString': messageString})
		else:
			return HttpResponseRedirect("/bookManiacs/profile/")
	else:
		return HttpResponseRedirect("/bookManiacs/login/")

def idGenerator(size=8):
	chars=string.ascii_letters + string.digits
	print chars
	return ''.join(random.choice(chars) for _ in range(size))

def makeValidation():
	return true

def sendEmail():
	code = idGenerator(8)
	print 'here'
	subject, from_email, to = 'hello', 'from@example.com', 'aksheshdoshi@gmail.com'
	text_content = 'This is an important message.'
	html_content = 'Here is the message.<br /> Here is the code: ' + code + '. Go to this <a href="http://localhost:8000/bookManiacs/">link</a>'
	msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
	msg.attach_alternative(html_content, "text/html")
	msg.send()