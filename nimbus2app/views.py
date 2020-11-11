from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
from .forms import *
# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/') 
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print(hashed_pw)
        new_user = User.objects.create(name=request.POST['name'], username=request.POST['username'],
        email=request.POST['email'], password=hashed_pw)
        request.session['user_id'] = new_user.id
        return redirect('/home')
    return redirect('/') 

def login(request):
    logged_user = User.objects.filter(email=request.POST['email'])
    if len(logged_user) > 0:
        logged_user = logged_user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect('/home')
    messages.error(request, "Email and/or password are incorrect")
    return redirect('/')

def logout(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    request.session.clear()
    return redirect('/')

def home(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'home.html', context)

def image_upload_view(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            img_obj = form.instance
            return render(request, 'home.html', {'form': form, 'img_obj': img_obj})
        else:
            form = ImageForm()
        return render(request, 'home.html', {'form': form})