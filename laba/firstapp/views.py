from django.shortcuts import render
from django.http import HttpResponse
from os import listdir, mkdir, rmdir
from os.path import isfile, join, isdir, dirname, realpath
import requests
import shutil

root_dir = join(dirname(realpath(__file__)),'test')

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
        shutil.rmtree(root_dir + request.path[:-7] + namefolder)
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
