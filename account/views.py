from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import *


from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages



@csrf_exempt
# Create your views here.
def registerPage(request):
    form= CreateUserForm()
    if request.method =='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'Account was created for '+ user)
            return redirect('login')

    context = { "form":form}
    return render(request , 'account/register.html',context)




@csrf_exempt
def loginPage(request):
   
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')   
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect(f'../../?id={username}')
            #127.0.0.1:8000/account/
            #../ -> 127.0.0.1:8000/
            #f'127.0.0.1:8000/?id={username}'
        else:
            messages.info(request,'Username or password is incorrect')
                
    content = {}
    return render(request , 'account/login.html',content)

def logoutUser(request):
    logout(request)
    return redirect('login')