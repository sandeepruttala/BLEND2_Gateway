from django.shortcuts import render
from users.models import CustomUser
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
import hashlib
import os
from .file_tools import save_file
from .ipfs_apis import retrieve, post_folder
# Create your views here.


def redirect_to_login(request):
    return redirect('login')


def login_(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')


def logout_(request):
    logout(request)
    return redirect('login')


def register_(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        password = request.POST.get('password')
        user = CustomUser(email=email, name=name)
        user.set_password(password)
        user.save()
        return redirect('login')
    return render(request, 'register.html')


def home(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'home.html')
    else:
        return redirect('login')


def upload(request):
    if request.method == 'POST':
        # get file from the request
        files = request.FILES.getlist('file')
        file_name = files[0].name
        folder_name = hashlib.sha256(file_name.encode()).hexdigest()
        media_path = f"media/{folder_name}"
        os.makedirs(media_path, exist_ok=True)
        for file in files:
            with open(f"media/{folder_name}/{file.name}", 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
        # extract metadata
        save_file(file_name, folder_name, request)
        status_retrieve = retrieve(folder_name)
        if status_retrieve != "False":
            post_folder(status_retrieve)
        else:
            return redirect('home')
    return redirect('home')









