from django.shortcuts import render
from users.models import CustomUser
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
import os
import datetime
import json
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
        files = request.FILES.getlist('file')
        folder_name = request.POST.get('folder_name')
        # print(folder_name)
        # print(files)
        # create a folder with the folder_name
        os.mkdir(f"media/{folder_name}")
        for file in files:
            with open(f"media/{folder_name}/{file.name}", 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
        # extract metadata
        extract_metadata(folder_name,request)
    return redirect('home')

def extract_metadata(folder_name,request):
    folder_info = os.stat(f"media/{folder_name}")
    print(folder_info)
    user = request.user
    folder_size = get_folder_size(f"media/{folder_name}")
    metadata = {
        "user_id": user.email,
        "folder_name": folder_name,
        "size": folder_size,
        "creation_date": datetime.datetime.fromtimestamp(folder_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
    }
    # create a json file with the metadata and save it in the folder
    with open(f"media/{folder_name}/{folder_name}_metadata.json", 'a') as f:
        json.dump(metadata, f, indent=4)

def get_folder_size(folder_path):
    total_size = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if not os.path.islink(file_path):  # Skip symbolic links
                total_size += os.path.getsize(file_path)
    return total_size