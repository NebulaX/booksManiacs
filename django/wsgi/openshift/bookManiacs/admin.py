from django.contrib import admin
from bookManiacs.models import Student_Year, Book, Profile, Item

admin.site.register(Book)
admin.site.register(Profile)
admin.site.register(Item)
# admin.site.register(User)

# class searchBox(admin.ModelAdmin):
# 	search_fields = ['author']