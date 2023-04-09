from django.db import models
from django import forms
from django.urls import reverse

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

def get_img_name(instance, filename):
    result = 'style/%s.png' % instance.name
    return result  

class Stylebase(models.Model):
    name = models.CharField(max_length=50)
    styleID = models.CharField(max_length=20)
    stylePrompt = models.CharField(max_length=255)
    style_preview = models.ImageField(upload_to=get_img_name, blank=False, null=False)
    scale = models.IntegerField(default=7)
    steps = models.IntegerField(default=50)
    def __str__(self):
        return self.name
    
class Userinfo(models.Model):
    
    name = models.CharField(max_length=50,blank=True,null=True)
    UserID = models.CharField(max_length=50,blank=True,null=True)
    head_shot = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.UserID

    def get_user_book(self):
        book =  Book.objects.filter(author = self.userinfo)
        return book



# 書本
class Book(models.Model):
    title = models.CharField(max_length=100,blank=True, null=True)
    author = models.CharField(max_length=100)
    like = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    book_category = models.CharField(max_length=50,null=True)
    published_date = models.DateField(auto_now=True)
    public_status = models.BooleanField(default=False)
    sid = models.CharField(max_length=20,blank=True, null=True)
    userinfo = models.ForeignKey(Userinfo, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse("book_id", kwargs={"id": self.name})
    
    def getCover(self):
        coverPage = Image.objects.filter(book=self).first()
        if coverPage:
            return coverPage.image
        # else 返回None
        return None


# 繪本圖片
class Image(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    page_number = models.PositiveSmallIntegerField()
    image = models.TextField(blank=True, null=True)
    prompt = models.CharField(max_length=255)
    height = models.IntegerField(default=512)
    width = models.IntegerField(default=512)
    steps = models.IntegerField(default=50)
    seeds = models.IntegerField(default=512, null=True)
    scale = models.IntegerField(default=7)
    description = models.TextField(blank=True, null=True)
    img_location = models.TextField(null=True)
    def __str__(self):
        return f"{self.page_number}"
    

