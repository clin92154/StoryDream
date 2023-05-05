from django.shortcuts import render , redirect
from django.shortcuts import redirect
from MakerSpace.models import * 
from django.http import JsonResponse ,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django import template
from django.template import loader ,Context
# Create your views here.

###########
# 顯示頁面 #
###########
@csrf_exempt
def showpage(request):
    bookID = Book.objects.get(id=int(request.POST.get('id'))) 
    #新頁面資訊顯示
    pages = Image.objects.get(book=bookID,page_number=request.POST.get('page'))
    setblock1 = loader.get_template('storyhall/showpage.html')
    c ={
        'book':bookID,
        'pages':pages,
    }
    return HttpResponse(setblock1.render(c))

###########
# 顯示繪本 #
###########
def showStory(request , *args, **kwargs):
    #取得已經公開繪本的ID
    book_id = int(kwargs['book_id'])
    book = Book.objects.get(id = book_id)
    pages = Image.objects.filter(book = book_id).order_by('page_number')
    content = {
        'book' : book,
        'pages' :pages
    }
    return render(request,'storyhall/story_view.html' , content)

########
# 瀏覽 #
########
def index(request):
    #取得已經公開繪本的ID、作者資訊
    # print(request.COOKIES.get("uid"))
    # print(request.COOKIES.get('is_login'))
    book = Book.objects.all()
    # book_cover =  Image.objects.all()
    content = {
        'books':book,
    }
    
    return render(request,'storyhall/index.html',content)
    #若選擇後post接收風格的設定
    #取得picturebookID、style prompt後重新導向至繪本建立頁面



