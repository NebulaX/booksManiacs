# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
import string
import random

from bookManiacs.models import Book, Item, Profile
from recaptcha.client import captcha

def books(request):
	books_available =  Book.objects.filter(admin_approved=True).order_by('avail_count')
	data = {'books_available': books_available}
	return render(request, 'bookManiacs/books.html', data)

def items(request, book_author):
	exist = Book.objects.filter(author=book_author).count()
	if exist:
		if request.session.get('user'):
			name = request.session.get('user')
			req_items = Item.objects.filter(name=book_author, buy_request=0).exclude(seller=name)
			own_items = Item.objects.filter(name=book_author, seller=name).count()
			if request.session.get('error'):
				errorString = request.session['error']
				messageString = ''
				del request.session['error']
			elif request.session.get('message'):
				messageString = request.session['message']
				errorString = ''
				del request.session['message']
			else:
				errorString = ''
				messageString = ''
			data = {'req_items' : req_items, 'book_author' : book_author, 'exist' : exist, 'name' : name, 'own_items' : own_items, 'messageString' : messageString, 'errorString' : errorString}
		else:
			req_items = Item.objects.filter(name=book_author)
			data = {'req_items' : req_items, 'book_author' : book_author, 'exist' : exist}
		return render(request, 'bookManiacs/items.html', data)
	else:
		return render(request, '404.html')
		#404page

def login(request):
	if 'user' in request.session:
		name = request.session['user']
		return HttpResponseRedirect('/')
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
					if 'next' in request.GET:
						next = request.GET['next']
						return HttpResponseRedirect(next)
					return HttpResponseRedirect("/")
				else:
					data = {'errorString': 'your username and password didnt match'}
					return render(request, 'bookManiacs/login.html', data)
			else:
				data = {'errorString': 'This id is not registered. Maybe you wanna <a href="/signup/">signup</a>'}
				return render(request, 'bookManiacs/login.html', data)
		else:
			# sendEmail()
			return render(request, 'bookManiacs/login.html')

def logout(request):
	if 'user' in request.session:
		del request.session['user']
		del request.session['name']
		return HttpResponseRedirect("/")
	else:
		# return Http404
		return HttpResponse('You have been successfull in finding a broken link..well you are lost<br /><a href="/">home</a>')

def signup(request):
	if 'user' in request.session:
		return HttpResponseRedirect("/")
	else:
		if 'name' in request.POST:
			name        = request.POST['name']
			email       = request.POST['email']
			phone       = request.POST['phone']
			password    = request.POST['pass']
			confirmPass = request.POST['confPass']
			bhawan      = request.POST['bhawan']
			room        = request.POST['room']
			userExist = Profile.objects.filter(email=email).exists()
			if userExist==False:
				# if makeValidation():
				if email!='' and phone!='' and name!='' and password == confirmPass:
					response = captcha.submit(  
						request.POST.get('recaptcha_challenge_field'),
						request.POST.get('recaptcha_response_field'),
						'6LeQqfESAAAAAEGkf7fPeKcnjKrZJwqqZ2P3Elan',
						request.META['REMOTE_ADDR'],)
					if response.is_valid:
						p = Profile.objects.create(name = name, email = email, password = password, mobile_number = phone, room_number = room, hostel = bhawan)
						messageString = 'you have registered successfully'
						return render(request, 'bookManiacs/login.html', {'messageString': messageString})
					else:
						errorString = 'please fill the captcha correctly'
				else:
					errorString = 'Please fill the form correctly'
			else:
				errorString = 'This Id is already registered'
			return render(request, 'bookManiacs/signup.html', {'errorString': errorString})
		else:
			return render(request, 'bookManiacs/signup.html')

def buy(request,bookId):
	if request.session.get('user'):
		buyer = request.session.get('user')
		exist = Item.objects.filter(pk=bookId).exists()
		if exist:
			item = Item.objects.get(pk=bookId)
			book = Book.objects.get(item=item)
			ibuyer = Profile.objects.get(email=buyer)
			alreadyBought = Item.objects.filter(name=book, buyer=ibuyer).exists()
			if alreadyBought==False:
				item.buyer = ibuyer
				item.buy_request = 1
				item.save()
				book.avail_count -= 1
				book.save()
				request.session['message'] = "Your request has been registered. We would be contacting you soon for the transaction."
			else:
				request.session['error'] = 'You have already requested this book. If you want more than one of this you can ask us when we contact you.'
			return HttpResponseRedirect('/items/' + book.author + '/')
		else:
			return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/login/')

def sell(request):
	if request.session.get('user'):
		messageString = ''
		if 'author' in request.POST:
			if request.POST['author'].find('(') != -1:
				name   = request.POST['author'].split('(')[0].split(' ')[0]
				author = request.POST['author'].split('(')[1].split(')')[0]
			else:
				author = request.POST['author']
				name   = 'unknown'
			edition = request.POST['edition']
			other   = request.POST['other']
			seller  = request.session.get('user')
			p = Profile.objects.get(email=seller)
			bookExists = Book.objects.filter(author=author, name=name).exists()
			if bookExists==False:
				authorExists = Book.objects.filter(author=author).exists()
				if authorExists:
					random = idGenerator(3)
					b = Book.objects.create(author=author + ' ' + random, name=name, avail_count=1)
				else:
					b = Book.objects.create(author=author, name=name, avail_count=1)
				i = Item.objects.create(name=b, edition = edition, seller = p, other_details = other)
				messageString = 'Since this book(author) is new to us it will be shown for sale after admin approval. Thank You'
				allBooks = Book.objects.order_by('author')
			else:
				b = Book.objects.get(author=author)
				i = Item.objects.create(name = b, edition = edition, seller = p, other_details = other)
				b.avail_count += 1
				b.save()
				if b.admin_approved:
					messageString = 'Your book has been added for sale.'
				else:
					messageString = 'Since this book(author) is new to us it will be shown for sale after admin approval. Thank You'
		books_available =  Book.objects.filter(admin_approved=True)
		return render(request, 'bookManiacs/sell.html', {'allBooks': books_available, 'messageString' : messageString})
	else:
		return HttpResponseRedirect('/')

def profile(request):
	if request.session.get('user'):
		name = request.session['user']
		sellerOf = Item.objects.filter(seller = name)
		buyerOf = Item.objects.filter(buyer = name)
		if request.session.get('error'):
			errorString = request.session['error']
			messageString = ''
			del request.session['error']
		elif request.session.get('message'):
			messageString = request.session['message']
			errorString = ''
			del request.session['message']
		else:
			errorString = ''
			messageString = ''
		data = {'sellerOf' : sellerOf,'buyerOf' : buyerOf, 'name' : name, 'errorString' : errorString, 'messageString' : messageString}
		return render(request, 'bookManiacs/profile.html', data)
	else:
		return HttpResponseRedirect("/login/")

def password(request):
	if request.session.get('user'):
		email = request.session['user']
		if 'oldPass' in request.POST:
			oldPass    = request.POST['oldPass']
			newPass    = request.POST['newPass']
			confPass   = request.POST['confPass']
			if newPass != confPass:
				data = {'errorString' : 'The two passwords you entered did not match.'}
				return render(request, 'bookManiacs/password.html', data)
			user = Profile.objects.get(email=email)
			realPassword = user.password
			if oldPass == realPassword:
				user.password = newPass
				user.save()
				return HttpResponseRedirect("/profile")
			else:
				data = {'errorString' : 'Entered wrong password.'}
				return render(request, 'bookManiacs/password.html', data)
		else:
			return render(request, 'bookManiacs/password.html')
	else:
		return HttpResponseRedirect("/")

def removeBuy(request, bookId):
	if request.session.get('user'):
		buyer = request.session.get('user')
		exist = Item.objects.filter(pk=bookId).count()
		if exist:
			p = Item.objects.get(pk=bookId)
			book = Book.objects.get(item=p)
			p.buyer = None
			p.buy_request = 0
			book.avail_count += 1
			p.save()
			book.save()
			request.session['message'] = 'The book has been removed from your buy list'
			return HttpResponseRedirect("/profile/")
		else:
			return HttpResponseRedirect("/profile/")
	else:
		return HttpResponseRedirect("/login/")

def removeBook(request, bookId):
	if request.session.get('user'):
		seller = request.session.get('user')
		exist = Item.objects.filter(pk=bookId).count()
		if exist:
			p = Item.objects.get(pk=bookId)
			book = Book.objects.get(item=p)
			p.delete()
			book.avail_count -= 1
			book.save()
			request.session['message'] = 'The book has been removed from your sell items'
		return HttpResponseRedirect('/profile/')
	else:
		return HttpResponseRedirect('/login/')

def idGenerator(size=8):
	chars=string.ascii_letters + string.digits
	return ''.join(random.choice(chars) for _ in range(size))

def makeValidation():
	return true

def sendEmail():
	code = idGenerator(8)
	subject, from_email, to = 'hello', 'from@example.com', 'aksheshdoshi@gmail.com'
	text_content = 'This is an important message.'
	html_content = 'Here is the message.<br /> Here is the code: ' + code + '. Go to this <a href="http://localhost:8000/">link</a>'
	msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
	msg.attach_alternative(html_content, "text/html")
	msg.send()