from django.shortcuts import render
from django.shortcuts import redirect
from MakerSpace.models import * 

# Create your views here.
##
# 顯示繪本
##
def showStory(request):
    #取得已經公開繪本的ID
    pass


##
# 瀏覽
##
def index(request):
    #取得已經公開繪本的ID、作者資訊
    username = request.GET.get("id")
    if username:
        return render(request,'storyhall/index.html')
    #若選擇後post接收風格的設定
    #取得picturebookID、style prompt後重新導向至繪本建立頁面



