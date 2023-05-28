from django.shortcuts import render, redirect
import requests
import torch
from diffusers import DiffusionPipeline, EulerDiscreteScheduler
from django.http import JsonResponse, HttpResponse

from django.urls import resolve
from deep_translator import GoogleTranslator

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django import template
from django.template import loader, Context
# 存檔案
from io import BytesIO
import base64
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from .models import *
# 給隨機seed
import random
import os
import replicate
# google translate
# from google_trans_new import google_translator
# 類別資料庫及關鍵字資料庫導入
categories = Category.objects.all()
promptBase = PromptBase.objects.all().values()
SIZE = [size for size in range(128, 1025, 128)]


# - 取得ID跟頁碼(e.g. 3
def ChangeLocation(request):
    # - 取得ID跟頁碼(e.g. 3
    bookID = Book.objects.get(id=int(request.POST.get('id')))
    page = Image.objects.filter(
        book=bookID, page_number=request.POST.get('page'))
    page.update(img_location=request.POST.get('location'))
    return JsonResponse({'status': True})
###########
# 創作頁面##
# ###########


@login_required(login_url='login')
@csrf_exempt
def makerspace(request, *args, **kwargs):
    if request.method == "POST":
        bookID = Book.objects.get(
            id=int(request.POST['book_Id']))  # session['bookID']
        bookID.sid = request.POST["style_Id"]
        bookID.save()
        pages = Image.objects.filter(book=bookID).order_by('page_number')
        count = sum(1 for i in pages)
        if not (count):
            styleID = Stylebase.objects.get(
                styleID=request.POST['style_Id'])  # 取得繪本ID
            steps = styleID.steps
            Image.objects.create(page_number=0, book=bookID, seeds=random.randint(
                1, 4294967295), steps=steps, img_location="area-left")
        print(1)
        return redirect(f'{bookID.id}/')
    print(0)
    bookID = Book.objects.get(id=int(kwargs['book_id']))
    pages = Image.objects.filter(book=bookID).order_by('page_number')
    context = {
        'book': bookID,
        'pages': pages,
        'promptBase': promptBase,
        'categories': categories,
        'height': SIZE,
        'width': SIZE,
    }
    # 若無圖片先以第一頁為預設
    print(2)
    return render(request, 'gallery/makerspace.html', context)

###################
# 顯示頁面
# ##################


@csrf_exempt
def showpage(request):

    bookID = Book.objects.get(id=int(request.POST.get('id')))  # 原頁面資訊儲存
    oldpage = Image.objects.filter(
        book=bookID, page_number=request.POST.get('old_page_num'))
    oldpage.update(description=request.POST.get('old_page_text'),
                   img_location=request.POST.get('old_page_cover'))
    # 新頁面資訊顯示
    pages = Image.objects.get(
        book=bookID, page_number=request.POST.get('page'))
    setblock1 = loader.get_template('makerspace/main.html')
    c = {
        'book': bookID,
        'pages': pages,
        'promptBase': promptBase,
        'categories': categories,
        'height': SIZE,
        'width': SIZE,
    }
    return HttpResponse(setblock1.render(c))

###################
# 移除功能
# ##################


@csrf_exempt
def remove(request):
    # - 取得ID跟頁碼(e.g. 3
    bookID = Book.objects.get(id=int(request.POST.get('id')))
    count = len(Image.objects.filter(book=bookID))
    if count > 1:
        #- 將該頁面進行移除
        Image.objects.filter(
            book=bookID, page_number=request.POST.get('page')).delete()
        pages = Image.objects.filter(
            book=bookID).order_by('page_number')  # 重新整理頁面
        #- 接著後面頁面的頁碼-1
        for page, item in enumerate(pages):
            item.page_number = page
            item.save()
    # item.update(page_number=int(page))
    pages = Image.objects.filter(book=bookID).order_by('page_number')  # 重新整理頁面
    templates = loader.get_template('makerspace/loadpages.html')
    context = {'pages': pages, 'book': bookID}
    return HttpResponse(templates.render(context))

###################
# 插入功能
# ##################


@csrf_exempt
def insert(request):
    bookID = Book.objects.get(id=int(request.POST.get('id')))
    pages = Image.objects.filter(book=bookID).order_by('page_number')
    new_page = sum(1 for i in pages)
    seed = Image.objects.get(book=bookID, page_number=new_page-1).seeds
    Image.objects.create(page_number=new_page, book=bookID, seeds=seed,
                         steps=70, img_location="area-top",description="")
    pages = Image.objects.filter(book=bookID).order_by('page_number')
    # 重新設定幾個網頁
    templates = loader.get_template('makerspace/loadpages.html')
    context = {'pages': pages, 'book': bookID}
    return HttpResponse(templates.render(context))


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


#######
# 新版本
#######
# @login_required(login_url='login')
@csrf_exempt
def generate(request):
    #取得bookID所綁定的style prompt
    print(request.POST['bid'])
    # translator = google_translator()
    bookID = Book.objects.get(id=request.POST['bid']) #session['bookID']
    pages = Image.objects.filter(book=bookID,page_number=request.POST['page'])
    if  is_ajax(request=request) and request.method == "POST":
        #只要生成圖像參數表單即可
        prompt = GoogleTranslator(source='auto', target='en').translate(request.POST['prompt'])#加上style
        scale = float(request.POST['scale'])
        seed = int(request.POST['seed'])
        steps = int(request.POST['steps'])
        print(prompt,scale,seed,steps,sep='\n')

    """
    seed : 能控制圖片生成的多樣性，
    step : 次數越多，文本推理步驟就越多
    SCALE:
    """

    #Set the REPLICATE_API_TOKEN environment variable
    os.environ["REPLICATE_API_TOKEN"] = "r8_RnsWfcJfBMbOyTZgcCq2gFDgQlX5RwE17zhV1"

    model = replicate.models.get("stability-ai/stable-diffusion")
    version = model.versions.get("db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf")
    # https://replicate.com/stability-ai/stable-diffusion/versions/db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf#input
    style = Stylebase.objects.get(styleID=str(bookID.sid))
    inputs = {
        'prompt': prompt + style.stylePrompt ,
        'image_dimensions': "768x768",
        'num_outputs': 1,
        'num_inference_steps': steps,
        'guidance_scale': scale,
        'scheduler': "DPMSolverMultistep",
        'seed':seed,
    }

    # https://replicate.com/stability-ai/stable-diffusion/versions/db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf#output-schema
    output = version.predict(**inputs)[0]
    response = requests.get(output)
    buffer = BytesIO(response.content)
    #取得目前繪本id資料夾，若沒有則建立並依據編號存到該路徑中
    image_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    pages.update(prompt=request.POST['prompt'],image=image_str, height=768, width=768,seeds=seed,steps=steps, scale= scale)
    return JsonResponse({'image_str': image_str})


###################
# 風格選擇頁面
# ##################
# 建立繪本ID-取得會員資料等

def style_choose(request, *args, **kwargs):
    # 取得繪本ID
    book = kwargs['book_id']

    # 導入風格資料庫
    style = Stylebase.objects.all()
    context = {'stylebase': style, 'book_id': book}
    # 若選擇後post接收風格的設定
    # 取得picturebookID、style prompt後重新導向至繪本建立頁面
    # 將繪本ID傳送至頁面
    return render(request, 'stylebase/style_choose.html', context)

# 建立繪本ID-取得會員資料等


@csrf_exempt
def book_create(request, *args, **kwargs):
    print(request.COOKIES.get("uid"))
    print(request.COOKIES.get('is_login'))
    if request.COOKIES.get('is_login'):
        userid = Userinfo.objects.get(UserID=request.COOKIES.get("uid"))
        book = Book.objects.create(author=userid, userinfo=userid,title='',description='')
        # 將繪本ID傳送至頁面
        return HttpResponse(f'makerspace/style_choose/{book.id}/')
    return HttpResponse('account/login')
    # else:
    #     uid = Userinfo.objects.get(UserID='guest')
