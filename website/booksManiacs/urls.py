from django.conf.urls import patterns, url

from booksManiacs import views

urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
	url(r'^books/', views.books, name='books')
)