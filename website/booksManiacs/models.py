from django.db import models

# Create your models here.

class Book(models.Model):
	name = models.CharField(max_length=100)
	author = models.CharField(max_length=40)
	edition = models.CharField(max_length=15)
	def __unicode__(self):
		return self.name

class Student_Year(models.Model):
    FIRST = '1st'
    SECOND = '2nd'
    THIRD = '3rd'
    FOURTH = '4th'
    YEAR_CHOICES = (
        (FIRST, 'First'),
        (SECOND, 'Second'),
        (THIRD, 'Third'),
        (FOURTH, 'Fourth'),
    )

class Profile(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField(max_length=254,primary_key=True)
	phone_number = models.CharField(max_length=10)
	room_number = models.CharField(max_length=10)
	year = models.CharField(max_length=3,choices=Student_Year.YEAR_CHOICES,default='')
	enrollment_number = models.CharField(max_length=8)
	books = models.ManyToManyField(Book)
	def __unicode__(self):
		return self.name

class User(models.Model):
	email = models.OneToOneField(Profile)
	password = models.CharField(max_length=32)