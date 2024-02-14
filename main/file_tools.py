import os
import datetime
import pytz
import json


def save_file(file_name, folder_name, request):
    user = request.user
    folder_size = get_folder_size(f"media/{folder_name}")
    metadata = {
        'file_name': file_name,
        "user_id": user.email,
        "size": folder_size,
        "upload_date_time": datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S"),
    }
    with open(f"media/{folder_name}/metadata.json", 'w') as f:
        json.dump(metadata, f, indent=4)


def get_folder_size(folder_path):
    total_size = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if not os.path.islink(file_path):
                total_size += os.path.getsize(file_path)
    return total_size
