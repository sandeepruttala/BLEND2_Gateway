from django.shortcuts import render
from users.models import CustomUser
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
import os
import datetime
import json
import hashlib
# Create your views here.
def login_(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

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
        folder_name = hashlib.md5(file_name.encode()).hexdigest()
        media_path = f"media/{folder_name}"
        os.makedirs(media_path, exist_ok=True)
        for file in files:
            with open(f"media/{folder_name}/{file.name}", 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
        # extract metadata
        extract_metadata(file_name,folder_name,request)
    return redirect('home')

def extract_metadata(file_name,folder_name,request):
    folder_info = os.stat(f"media/{folder_name}")
    # print(folder_info)
    user = request.user
    folder_size = get_folder_size(f"media/{folder_name}")
    metadata = {
        'file_name': file_name,
        "user_id": user.email,
        "size": folder_size,
        "creation_date": datetime.datetime.fromtimestamp(folder_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
    }
    with open(f"media/{folder_name}/metadata.json", 'a') as f:
        json.dump(metadata, f, indent=4)

def get_folder_size(folder_path):
    total_size = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if not os.path.islink(file_path):
                total_size += os.path.getsize(file_path)
    return total_size