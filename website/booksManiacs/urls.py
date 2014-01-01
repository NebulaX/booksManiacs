from django.conf.urls import patterns, url

from booksManiacs import views

urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
	url(r'^books/$', views.books, name='books'),
	url(r'^items/(?P<book_author>[\w\s]+)/$', views.items, name='items'),
	# url(r'^signup/$', views.signup, name='signup'),
	# url(r'^signout/$', views.signout, name='signout'),
	# url(r'^', views., name=''),
	# url(r'', views., name=''),
)