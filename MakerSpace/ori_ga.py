# 判斷是否為ajax事件
# ##################
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
###################
# 生圖
# ##################
# @login_required(login_url='login')
# @csrf_exempt
# def generate(request):
#     #取得bookID所綁定的style prompt
#     print(request.POST['bid'])
#     bookID = Book.objects.get(id=request.POST['bid']) #session['bookID']
#     pages = Image.objects.filter(book=bookID,page_number=request.POST['page'])
#     if  is_ajax(request=request) and request.method == "POST":
#         #只要生成圖像參數表單即可
#         prompt = request.POST['prompt'] #加上style
#         scale = float(request.POST['scale'])
#         seed = int(request.POST['seed'])
#         steps = int(request.POST['steps'])
#         height = int(request.POST['height'])
#         width =  int(request.POST['width'])
#         print(prompt,scale,seed,steps,sep='\n')

#     device = "cuda" if torch.cuda.is_available() else 'cpu'
#     model_id = "stabilityai/stable-diffusion-2"
#     auth_token = "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"

#     scheduler = EulerDiscreteScheduler.from_pretrained(
#         model_id, subfolder="scheduler")
#     pipe = DiffusionPipeline.from_pretrained(
#         model_id, use_auth_token=auth_token, scheduler=scheduler).to(device)
#     # use_auth_token = auth_token
#     # with autocast(device):

#     """
#     seed : 能控制圖片生成的多樣性，
#     step : 次數越多，文本推理步驟就越多
#     SCALE:
#     """

#     generator = torch.Generator(device).manual_seed(seed)  # seed設定，seed越高
#     image = pipe(prompt,  height=height, width=width, guidance_scale=scale,
#                  num_inference_steps=steps, generator=generator).images[0]


    # #取得目前繪本id資料夾，若沒有則建立並依據編號存到該路徑中
    # # image.save(f'media/image/tmp.png')
    # # PATH = settings.MEDIA_ROOT + '/image/tmp.png'
    # buffer = BytesIO()
    # image.save(buffer, format="PNG")
    # image_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    # pages.update(prompt=prompt,image=image_str, height=height, width=width,seeds=seed,steps=steps, scale= scale)
    # return JsonResponse({'image_str': image_str})
    # # return HttpResponse(f'<img src="data:image/png;base64,{image_str}"/>')
