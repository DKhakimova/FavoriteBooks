from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, 'index.html')

def create(request):
    errors = User.objects.validate(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    
    new_user = User.objects.register(request.POST)
    request.session['user_id'] = new_user.id
    messages.success(request, "Successfully registered!")
    return redirect('/')

def login(request):
    result = User.objects.authenticate(request.POST['email'], request.POST['password'])
    if result == False:
        messages.error(request, "Invalid Credentials")
    
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
        messages.success(request, "Successfully logged in!")
        return redirect('/books')
    return redirect('/')

def success(request):
    if not 'user_id' in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'success.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')