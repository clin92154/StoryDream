from django.shortcuts import render, redirect
import torch
from diffusers import DiffusionPipeline, EulerDiscreteScheduler
from django.http import JsonResponse ,HttpResponse

from django.urls import resolve


from django.views.decorators.csrf import csrf_exempt
from django import template
from django.template import loader ,Context
#存檔案
from io import BytesIO
import base64
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from .models import *
#給隨機seed
import random


#類別資料庫及關鍵字資料庫導入
categories = Category.objects.all()
promptBase = PromptBase.objects.all().values()
SIZE = [size for size in range(128,1025,128)]


###################
# 創作頁面
# #################
@csrf_exempt
def makerspace(request):
    if request.method == "POST":
        bookID = Book.objects.get(id=request.POST.get('bookID')) #session['bookID']
        pages = Image.objects.filter(book=bookID).order_by('page_number') 
        count = sum(1 for i in pages)
        if not(count):
            styleID = stylebase.objects.get(styleID=request.POST.get('styleID')) #取得繪本ID
            steps = styleID.steps
            Image.objects.create(page_number=0,book=bookID,seeds=random.randint(1,4294967295),steps=steps)

    context = {
        'pages':pages,
        'promptBase': promptBase,
        'categories': categories,
        'height': SIZE,
        'width': SIZE,
    }
    #若無圖片先以第一頁為預設

    return render(request, 'gallery/makerspace.html', context)

################### 
# 顯示頁面 
# ##################
@csrf_exempt
def showpage(request):
    bookID = Book.objects.get(bookID=request.POST.get('id'))
    #原頁面資訊儲存
    oldpage =  Image.objects.filter(book=bookID,page_number=request.POST.get('old_page_num'))
    oldpage.update(description=request.POST.get('old_page_text'))
    #新頁面資訊顯示
    pages = Image.objects.get(book=bookID,page_number=request.POST.get('page'))
    setblock1 = loader.get_template('makerspace/main.html')
    c ={
        'pages':pages,
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
    #- 取得ID跟頁碼(e.g. 3
    bookID = Book.objects.get(bookID=request.POST.get('id'))
    page_num = int(request.POST.get('page'))
    if len(Image.objects.filter(book=bookID))>1:
        #- 將該頁面進行移除
        Image.objects.filter(book=bookID,page_number=request.POST.get('page')).delete() 
        pages = Image.objects.filter(book=bookID).order_by('page_number') #重新整理頁面
        #- 接著後面頁面的頁碼-1
        for page,item in enumerate(pages):
            item.page_number=page
            item.save()
    # item.update(page_number=int(page))
    pages = Image.objects.filter(book=bookID).order_by('page_number') #重新整理頁面
    templates = loader.get_template('makerspace/loadpages.html')
    context= {'pages':pages}
    return HttpResponse(templates.render(context))       

###################
# 插入功能
# ##################
@csrf_exempt
def insert(request):
    bookID = Book.objects.get(bookID=request.POST.get('id'))
    pages = Image.objects.filter(book=bookID).order_by('page_number')
    new_page = sum(1 for i in pages)
    seed = Image.objects.get(book=bookID,page_number=new_page-1).seeds
    Image.objects.create(page_number=new_page,book=bookID,seeds=seed,steps=70,prompt="可自行輸入圖片的關鍵字或透過上方類別選擇!")
    pages = Image.objects.filter(book=bookID).order_by('page_number')
    #重新設定幾個網頁
    templates = loader.get_template('makerspace/loadpages.html')
    context= {'pages':pages}
    return HttpResponse(templates.render(context))


###################
# 判斷是否為ajax事件
# ##################
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


###################
# 生圖
# ##################
@csrf_exempt
def generate(request):
    #取得bookID所綁定的style prompt
    bookID = Book.objects.get(bookID='1234567') #session['bookID']
    pages = Image.objects.filter(book=bookID,page_number=request.POST['page'])
    if  is_ajax(request=request) and request.method == "POST":
        #只要生成圖像參數表單即可
        prompt = request.POST['prompt'] #加上style
        scale = float(request.POST['scale'])
        seed = int(request.POST['seed'])
        steps = int(request.POST['steps'])
        height = int(request.POST['height'])
        width =  int(request.POST['width'])
        print(prompt,scale,seed,steps,sep='\n')

    device = "cuda" if torch.cuda.is_available() else 'cpu'
    model_id = "stabilityai/stable-diffusion-2"
    auth_token = "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"

    scheduler = EulerDiscreteScheduler.from_pretrained(
        model_id, subfolder="scheduler")
    pipe = DiffusionPipeline.from_pretrained(
        model_id, use_auth_token=auth_token, scheduler=scheduler).to(device)
    # use_auth_token = auth_token
    # with autocast(device):

    """
    seed : 能控制圖片生成的多樣性，
    step : 次數越多，文本推理步驟就越多
    SCALE:
    """

    generator = torch.Generator(device).manual_seed(seed)  # seed設定，seed越高
    image = pipe(prompt,  height=height, width=width, guidance_scale=scale,
                 num_inference_steps=steps, generator=generator).images[0]


    #取得目前繪本id資料夾，若沒有則建立並依據編號存到該路徑中
    # image.save(f'media/image/tmp.png')
    # PATH = settings.MEDIA_ROOT + '/image/tmp.png'
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    image_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    pages.update(prompt=prompt,image=image_str, height=height, width=width,seeds=seed,steps=steps, scale= scale)
    return JsonResponse({'image_str': image_str})
    # return HttpResponse(f'<img src="data:image/png;base64,{image_str}"/>')


################### 
# 風格選擇頁面
# ##################
#建立繪本ID-取得會員資料等
def style_choose(request,*args,**kwargs):
    #取得繪本ID
    bookid = kwargs['book_id'].split('_')[1]

    #導入風格資料庫
    style = stylebase.objects.all()
    context = {'stylebase': style,'book_id':bookid}
    #若選擇後post接收風格的設定
    #取得picturebookID、style prompt後重新導向至繪本建立頁面
    return render(request,'stylebase/style_choose.html',context) #將繪本ID傳送至頁面

#建立繪本ID-取得會員資料等
@csrf_exempt
def book_create(request):
    book = Book.objects.create(author=request.POST.get("id"))
    return HttpResponse(f'makerspace/style_choose/{book}/') #將繪本ID傳送至頁面
