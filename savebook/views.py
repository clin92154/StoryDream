from django.shortcuts import render
from django.http import JsonResponse ,HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from MakerSpace.models import *
# Create your views here.
@csrf_exempt
def save(request , *args, **kwargs):
    if request.method == "POST":
        if request.POST['public_status'] == 'private':
            status = False
        else:
            status = True
        book_id = int(kwargs['book_id'])
        book = Book.objects.filter(id = book_id)
        book.update(title=request.POST['book_title'],description=request.POST['description'],public_status=status)
        #,cover_page =request.POST['cover_page']
        ID = Book.objects.get(id = book_id).author

        return redirect(f'../../../?id={ID}')  
    
@csrf_exempt
def savebook(request,*args, **kwargs):
    book_id = int(kwargs['book_id'])
    book = Book.objects.get(id = book_id)
    cover_page = Image.objects.get(book=book_id , page_number = 0)
    pages = len(Image.objects.filter(book=book_id))
    settings={
        'book':book,
        'cover_page':cover_page,
        'pages':pages
    }
    return render(request,'savebook/save.html',settings)