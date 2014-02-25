from django.conf.urls import patterns, url
from booksManiacs import views

# handler404 = 'django.views.defaults.page_not_found'

urlpatterns = patterns('',
	url(r'^$', views.books, name='books'),
	url(r'^home/$', views.home, name='home'),
	url(r'^items/(?P<book_author>[\w\s]+)/$', views.items, name='items'),
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^login/$', views.login, name='login'),
	url(r'^buy/(?P<bookId>\d+)/$', views.buy, name='buy'),
	url(r'^sell/$', views.sell, name='sell'),
	# url(r'^/$', views., name=''),
)