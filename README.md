booksManiacs
============
Instructions:

1) Open website/website/settings.py and under databases change the value of the variable NAME according to your directory 	where your website/database folder is on your local machine.Then run 
		python manage.py syncdb
	in your shell in the website directory where manage.py file is present.


Working:

run "python manage.py runserver" to see the site working

1) for front end (html pages)
    go to website/booksManiacs/templates/booksManiacs/
	this directory has all the html pages.You can see the url of the page from website/booksManiacs/urls.py

2) database changes
    for making changes in database go to "127.0.0.1/admin" your browser (this will work after the runserver command only)
	username : full name like "aksheshdoshi"
	password : first name like "akshesh" (both without quotes)
	change your password from the option in the top-right corner and commit these changes else your password will be lost the next time you pull or clone.

3) website's pages:
	see the website's homepage at "127.0.0.1/booksManiacs/"
	you can get the links for the other pages from the urls.py mentioned in first point.