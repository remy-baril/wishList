from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages

##index page renders template w forms on it
def index(request):
    if 'user_id' not in request.session:
        return render(request, 'wishBeltApp/index.html')
    else:
        return redirect('/dashboard')

def register(request):
    resp = User.objects.regValidation(request.POST) ##stores response you get from register method in manager
    if resp['status']: ##status is true or false whether there were messages or not
        user = User.objects.createUser(request.POST) ## creates user w data and stores their info into user variable
        request.session['user_id'] = user.id ##adds id to session
        return redirect('/dashboard')
    else:
        for error in resp['errors']:
            messages.error(request,error)
        return redirect ('/')

def login(request):
    user = User.objects.login(request.POST) ##finds login method in User model and passes data into it
    if user:
        request.session['user_id'] = user.id ##if a user is returned, stores user id into session id method
        return redirect('/dashboard') ##route to home page
    messages.error(request, 'Username or password is invalid') ## if no user found, flashes this error
    return redirect('/')

def logout(request):
    request.session.clear() ##clears session
    return redirect('/')

def dashboard(request):
    currentUser = User.objects.get(id=request.session['user_id'])
    otherUsers = User.objects.all()
    wishedItem = currentUser.wished_item.values_list('id', flat=True) 
    exclude = Item.objects.exclude(id__in=wishedItem) 
    data = {
        'userData': currentUser,
        'items': exclude,
        'otherUsers': otherUsers
    }
    return render(request, 'wishBeltApp/dashboard.html', data)

def addPage(request):
    return render(request, 'wishBeltApp/addPage.html')

def addItem(request):
    resp = Item.objects.itemValidation(request.POST)
    if resp['status']:
        item = Item.objects.createItem(request.POST, request.session['user_id'])
        return redirect('/dashboard')
    else:
        for error in resp['errors']:
            messages.error(request,error)
        return redirect('/add')

def itemPage(request):
    return render(request, 'wishBeltApp.itemPage.html')

def deleteItem(request, item_id):
    Item.objects.deleteItem(item_id, request.session['user_id'])
    return redirect('/dashboard')