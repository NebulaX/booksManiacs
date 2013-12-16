from django.conf.urls import patterns, url

from booksManiacs import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	# url(r'^books/', views.books, name='books')
)