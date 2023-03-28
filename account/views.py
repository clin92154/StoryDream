from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from .forms import *
from .models import Userinfo
from MakerSpace.models import Book


from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from MakerSpace.models import *


@csrf_exempt
# Create your views here.
def registerPage(request):
    form= CreateUserForm()
    if request.method =='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            UserID = Userinfo.objects.create(UserID=user)
            messages.success(request,'Account was created for '+ user)
            return redirect('login')

    context = { "form":form}
    return render(request , 'account/register.html',context)




@csrf_exempt
def loginPage(request):
   
    if request.method == 'POST':
        uid= request.POST.get('username')
        password = request.POST.get('password')   
        user = authenticate(request,username=uid, password=password)
        if user is not None:

            login(request,user)
            userID = Userinfo.objects.get(UserID=uid)
            rep = redirect(f'../{userID}/')
            rep.set_cookie("is_login", True)
            rep.set_cookie("uid", userID)
            return rep
            # return redirect(f'../../?id={username}')
            #127.0.0.1:8000/account/
            #../ -> 127.0.0.1:8000/
            #f'127.0.0.1:8000/?id={username}'
        else:
            messages.info(request,'Username or password is incorrect')
    return render(request , 'account/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')


# def style_choose(request

    # book = kwargs['book_id']

# "<book_id>/""

#  {% csrf_token %}
@login_required(login_url='login')
def accountCenter(request,*args,**kwargs):

    status = request.COOKIES.get('is_login')

    if status:
        userID = Userinfo.objects.get(UserID=kwargs['uid'])
        # request.POST.get('username')
        book = Book.objects.filter(userinfo=userID)
        context = {
            'UserID' : userID,
            'books' : book
        }
        # userID = request.POST.get('username')
        # book = Book.objects.all()
        # userinfo =Userinfo.objects.all()
        # context = {'userinfo': userinfo,
        #            'book_id':book}     
        # 
        rep = render(request ,'account/member.html',context)      
        # rep.set_cookie("is_login", True)
        # rep.set_cookie("uid", userID)
        return rep
    return redirect('login')