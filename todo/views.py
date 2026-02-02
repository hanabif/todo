from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from todo import models
from todo.models import TODOO
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        emailid = request.POST.get('emailid')
        pwd = request.POST.get('pwd')

        my_user = User.objects.create_user(fnm,emailid,pwd)
        my_user.save()
        return redirect('/loginn')
    
    return render(request,'signup.html')

def loginn(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
        userr = authenticate(request,username = fnm, password = pwd)
        if userr is not None:
            login(request, userr)
            return redirect('/todopage')
        else:
            return redirect('/loginn')

    return render(request, 'login.html')

@login_required(login_url='/loginn')
def todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        obj = models.TODOO(title = title, user = request.user)
        obj.save()
        res = models.TODOO.objects.filter(user = request.user).order_by('-date')
        return redirect('/todopage')
    res = models.TODOO.objects.filter(user = request.user).order_by('-date')
    return render(request, 'todo.html', {'res': res}) 

@login_required(login_url='/loginn')
def edit_todo(request, srno):
    obj = models.TODOO.objects.get(srno=srno, user=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        obj.title = title
        print(obj.title)
        obj.save()
        return redirect('/todopage')

    res = models.TODOO.objects.filter(user=request.user).order_by('-date')
    return render(request, 'edit_todo.html', {
        'obj': obj,
        'res': res,
        'editing': True
    })

def delete_todo(request, srno):
    obj = models.TODOO.objects.get(srno=srno, user=request.user)
    obj.delete()
    return redirect('/todopage')

def signout(request):
    logout(request)
    return redirect('/loginn')