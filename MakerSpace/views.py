from django.shortcuts import render, redirect
import torch
from diffusers import DiffusionPipeline, EulerDiscreteScheduler
from django.http import JsonResponse , HttpResponse
from django.views.decorators.csrf import csrf_exempt

#存檔案
from io import BytesIO
import base64
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from .models import *
from gallery import settings
#給隨機seed
import random



SIZE = [size for size in range(128,1025,128)]
# Create your views here.


def pagesToDictionary(pages):
    output = {}
    output["book"] = pages.book
    output["page_number"] = pages.page_number
    output["image"] = pages.image
    output["prompt"] = pages.prompt
    output["height"] = pages.height
    output["width"] = pages.width
    output["steps"] = pages.steps
    output["seeds"] = pages.seeds
    output["scale"] = pages.scale
    output["description"] = pages.description

    return output


def insert(request):
    bookID = Book.objects.get(bookID=request.POST.get('id'))
    pages = Image.objects.filter(book=bookID).order_by('page_number')
    new_page = sum(1 for i in pages)
    seed = Image.objects.get(book=bookID,page_number=sum(1 for i in pages)-1).seeds
    Image.objects.create(page_number=new_page,book=bookID,seeds=seed,steps=70,prompt="可自行輸入圖片的關鍵字或透過上方類別選擇!")
    pages = list(pages.values())
    return JsonResponse({'pages':pages})

def index(request):
    # if session['bookID'] not in database:
     # bookID = new ID
    # else:
     # bookID = 12345678 #session['bookID']
    # image = PromptBase.objects.all().values()
    bookID = Book.objects.first() #session['bookID']
    pages = Image.objects.filter(book=bookID).order_by('page_number') 
    count = sum(1 for i in pages)
    
    #類別資料庫及關鍵字資料庫導入
    categories = Category.objects.all()
    promptBase = PromptBase.objects.all().values()
    if not(count):
        pages = Image.objects.create(page_number=0,book=bookID,seeds=random.randint(1,100000000),steps=70,prompt="可自行輸入圖片的關鍵字或透過上方類別選擇!")
    setting = {
        'pages':pages ,
        'promptBase': promptBase,
        'categories': categories,
        'height': SIZE,
        'width': SIZE,
    }
    #若無圖片先以第一頁為預設
   
    return render(request, 'gallery/index.html', setting)


from django.shortcuts import HttpResponse


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def generate(request):
    #request.is_ajax() and
    bookID = Book.objects.first() #session['bookID']
    pages = Image.objects.filter(book=bookID).order_by('page_number') 
    if  is_ajax(request=request) and request.method == "POST":
        #只要生成圖像參數表單即可
        prompt = request.POST['prompt']
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

    Picturebookid = 'pb20230202_1'

    #取得目前繪本id資料夾，若沒有則建立並依據編號存到該路徑中
    # image.save(f'media/image/tmp.png')
    # PATH = settings.MEDIA_ROOT + '/image/tmp.png'
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    image_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    # return JsonResponse({'image_str': image_str})
    return HttpResponse(f'<img src="data:image/png;base64,{image_str}"/>')



#建立繪本ID-取得會員資料等
def book_create(request):
    # picturebook_ID = 'AAAA_20230202_1' #產生會員亂碼_日期_第幾本
    # Picturebook = Picturebook() #新物件儲存繪本ID、作者(暫時不用)
    # Picturebook(picturebook_ID = picturebook_ID)
    # Picturebook.save()
    # request.session['picturebook_ID'] = picturebook_ID
    #取得picturebookID後重新導向至風格頁面
    return redirect('/gallery/style_choose.html') #將繪本ID傳送至頁面

#建立繪本ID-取得會員資料等
def style_choose(request):
    #取得繪本ID
    #導入風格資料庫
    #若選擇後post接收風格的設定
    #取得picturebookID、style prompt後重新導向至繪本建立頁面
    return redirect('/style/style_choose.html') #將繪本ID傳送至頁面
