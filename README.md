booksManiacs
============
Instructions:
----------------------------

Source Code of the website built for our project bookManiacs using Django Web Framework

###Dependencies
----------------------------
* [Python 2.7.](http://www.python.org)
* [Web Framework Django.](https://www.djangoproject.com/)

###Configuration
----------------------------
* Clone this repository to your local machine
* In the **website** directory of the root folder create a file named `dbConfig`
* Open `dbConfig` using any text editor and enter the full path of the file `booksManiacs.sqlite3` present in the database folder (refer to dbConfig.sample)
 
###Starting Server
---------------------------- 
* Navigate to the **website** directory in your root folder through command line i.e the folder where `manage.py` is present . 
* Run *python manage.py runserver*
* To test the setup navigate to [127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
* If configuration is done properly, a login dialog will appear. Use the following credentials :

`Username`: Your full name eg. *aksheshdoshi*

`Password`: Your first name eg. *akshesh*


###Usage
----------------------------
#####For Front End (html Pages)
* Navigate to `website/booksManiacs/templates/booksManiacs`

This directory has all the html pages . You can see the url of the page from 
*website/booksManiacs/urls.py*


#####Database Changes
* For making changes in the database go to [127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) and login as explained above . 
* Remember to change you password and commit these changes to the repository


#####Web Pages
* The url of the homepage is [127.0.0.1:8000/booksManiacs](http://127.0.0.1:8000/booksManiacs)
* Url's of other pages can be obtained from the `urls.py` mentioned above


###License
----------------------------
MIT Licensed

Copyright (C) 2014 NebulaX