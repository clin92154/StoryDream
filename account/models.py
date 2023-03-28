from django.db import models
from MakerSpace.models import *


# Create your models here.
# class Userinfo(models.Model):
#     UserID = models.CharField(max_length=50,blank=True,null=True)
#     head_shot = models.ImageField(blank=True, null=True)
#     book = models.ForeignKey(Book,on_delete=models.CASCADE)

#     def get_user_book(self):
#         pass
#     #get_user_book : datatype -> [book1,book2] -> return list
#         #for book in user.get_user_book:
#             # book.getCover book.id
