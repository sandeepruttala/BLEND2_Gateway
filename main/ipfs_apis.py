import requests
import os
import json


def retrieve(folder_name):
    media_path = f"/Users/sandeepruttala/Work/BLEND_gateway/media/{folder_name}"
    return upload_directory_to_ipfs(media_path)


def upload_directory_to_ipfs(directory_path, url='http://127.0.0.1:5001/api/v0/add'):
    # Ensure the directory exists
    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        print(f"Directory '{directory_path}' does not exist or is not a directory.")
        return

    # Prepare the files for upload
    files = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            files.append(('file', (filename, open(file_path, 'rb'))))

    if not files:
        print("No files to upload in the directory.")
        return

    # Send the POST request with 'wrap-with-directory' parameter
    response = requests.post(url, files=files, params={'wrap-with-directory': 'true'})

    # Close the files
    for _, file_tuple in files:
        file_tuple[1].close()

    # Handle the response
    if response.status_code == 200:
        # print("Directory uploaded successfully.")
        # print(response.text)
        response_list = response.text.split()
        # print(json.loads(response_list[-1])['Hash'])
        return json.loads(response_list[-1])['Hash']

    else:
        return "False"


def post_folder(cid):
    url = f'http://10.10.11.126:8000/upload/{cid}'
    response = requests.post(url)
    print(response.text)


def get_folder(cid):
    url = f'http://10.10.11.126:8000/retrieve/{cid}'
    response = requests.get(url)
    print(response.text)