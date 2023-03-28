from django.contrib import admin
from .models import *
from MakerSpace.admin import *
from MakerSpace.models import *

# Register your models here.

# class BookInline(admin.TabularInline):
#     model = Book
#     extra = 1

# class UserInfoAdmin(admin.ModelAdmin):
    
#     list_display = ['UserID','head_shot']
# admin.site.register(Userinfo, UserInfoAdmin)