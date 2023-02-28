from django.db import models
from django import forms
from django.urls import reverse
# Create your models here.


# class MakerSpace(models.Model):
#     prompt = models.CharField(max_length=255)  #prompt

# class Member(models.model):
#     memberID 
#     password 
#     email = models.EmailField()


# class Member_space(models.Model):
#      picturebook_ID = models.CharField(max_length=255,null=False)
#      bookshielf_ID = models.CharField(max_length=255,null=False)

## 關鍵字種類
class Category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'


    def __str__(self):
        return self.name

## 關鍵字資料庫
class PromptBase(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE
                                 ,related_name='promptbase')
    keyword = models.CharField(max_length=200, db_index=True)
    class Meta:
        ordering = ('category','keyword')

    def getCategory(self):
        return self.category

# 書本
class Book(models.Model):
    title = models.CharField(max_length=100,blank=True, null=True)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    published_date = models.DateField(auto_now=True)
    
    def __str__(self):
        return "%s_%s" % (self.author,self.id)
    
    def get_absolute_url(self):
        return reverse("book_id", kwargs={"id": self.name})


# 繪本圖片
class Image(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    page_number = models.PositiveSmallIntegerField()
    image = models.TextField(blank=True, null=True)
    prompt = models.CharField(max_length=255)
    height = models.IntegerField(default=512)
    width = models.IntegerField(default=512)
    steps = models.IntegerField(default=50)
    seeds = models.IntegerField(default=222222222, null=True)
    scale = models.IntegerField(default=7)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.book}_page_{self.page_number}"
    
class stylebase(models.Model):
    name = models.CharField(max_length=50)
    styleID = models.CharField(max_length=20)
    stylePrompt = models.CharField(max_length=255)
    scale = models.IntegerField()
    steps = models.IntegerField()
    def __str__(self):
        return self.name