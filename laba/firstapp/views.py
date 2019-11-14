from django.shortcuts import render
from django.http import HttpResponse
from os import listdir, mkdir, rmdir
from os.path import isfile, join, isdir, dirname, realpath
import requests

root_dir = join(dirname(realpath(__file__)),'test')
save_path = '' #you must indicate here the path where you want to download the file

def get_file_names(directory_path):
    return [f for f in listdir(directory_path) if isfile(join(directory_path, f))]

def get_dir_names(directory_path):
    return [d for d in listdir(directory_path) if isdir(join(directory_path, d))]

def main_window(request):
    result = "<b>Directories: </b>" + ' ,'.join(map(str,get_dir_names(root_dir))) +"<p><b>Files: </b>" + ','.join(map(str,get_file_names(root_dir)))+ "</p>"
    return HttpResponse(result)

def show_files(request):
    try:
        result = "<b>Directories: </b>" + ' ,'.join(map(str,get_dir_names(root_dir + request.path))) +"<p><b>Files: </b>" + ','.join(map(str,get_file_names(root_dir + request.path)))+ "</p>"
        return HttpResponse(result)
    except FileNotFoundError:
        return HttpResponse("<b>This folder does not exist.</b>")
    except NotADirectoryError:
        return HttpResponse("<b>This is not a directory.</b>")

def delete(request):
    namefolder = request.GET.get("foldername", "")
    try:
        rmdir(root_dir + request.path[:-7] + namefolder)
    except OSError:
        return HttpResponse("<b>Delete directory failed</b>")
    else:
        return HttpResponse("<b>Successfully deleted directory</b>")

def create(request):
    namefolder = request.GET.get("foldername", "")
    try:
        mkdir(root_dir + request.path[:-7] + namefolder)
    except OSError:
        return HttpResponse("<b>Create directory failed</b>")
    else:
        return HttpResponse("<b>Successfully created directory</b>")

def download(request): #boot from server
    namefile = request.GET.get("filename", "")
    path = root_dir + request.path[:-9] + namefile
    print(path)
    file = open(path,"r")
    response = HttpResponse(file,content_type='application/msword')
    response['Content-Disposition'] = 'attachment; filename=' + namefile
    return response

def upload(request): #upload to server
    if request.method == 'POST':
        if save_path == '':
            return HttpResponse("<b>Specify the path where you want to download the file</b>")
        else:
            with open(save_path + request.FILES['document'].name, 'wb+') as destination:
                for chunk in request.FILES['document'].chunks():
                    destination.write(chunk)
    return HttpResponse("<b>Success</b>")
    if request.method == 'GET':
        return render(request,'upload.html')
