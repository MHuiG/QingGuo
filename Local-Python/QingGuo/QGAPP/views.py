import json
import os
import time
from numpy import *
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from QGAPP.models import Record
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def About(request):
    return render(request, 'about.html')
def Study(request):
    return render(request, 'study.html')
def Gallery(request):
    return render(request, 'gallery.html')
def Home(request):
    return render(request, 'home.html')
def Schedule(request):
    return render(request, 'schedule.html')


def SaveRecord(request):
    try:
        result = request.POST.get("result")
        source = request.POST.get("source")
        rec = Record()
        rec.En = source
        rec.name = result
        rec.timestamp = time.time()
        rec.time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        rec.save()
        response = HttpResponse("OK")
    except Exception as e:
        print(e)
        response = HttpResponse("SYSTEM ERROR")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def GetSchedule(request):
    try:
        url = request.POST.get("url")
        rec = Record.objects.all()
        s = ""
        for i in rec.all():
            if i.name != "":
                #print(i.name,i.time)
                s = "<div>\r\n" + "<p><strong><a href='"+str(url)+"/" \
                            "studyVideo/?video=" + i.En+"'>" + i.name + "</a></strong></p>\r\n" + "<p>" \
                                + i.time + "</p>\r\n" + "</div>" + s
        response = HttpResponse(s)
    except Exception as e:
        print(e)
        response = HttpResponse("SYSTEM ERROR")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def StudyVideo(request):
    video=request.GET.get("video")
    context = {}
    context['video'] = video
    return render(request, 'study2.html', context)


def GetStudyVideo(request):
    try:
        rec = Record.objects.all()
        TimeNow = time.time()
        times = rec.all()[len(rec.all()) - 1].timestamp
        Ename = rec.all()[len(rec.all()) - 1].En
        if TimeNow >= float(times)-1 and TimeNow <= float(times)+1:
            flag = 1
        else:
            flag = 0
        response = HttpResponse(json.dumps({'Ename':Ename,'flag':flag}))
    except Exception as e:
        print(e)
        response = HttpResponse("SYSTEM ERROR")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def ReadFile(path,x):
    f = open(path, 'r', encoding='UTF-8')
    while True:
        i = f.readline()
        if not i:
            break
        x.append(i.strip())
    f.close()
    return x

def TextCat(request):
    try:
        x = []
        y = []
        code = []
        x = ReadFile(os.path.join(BASE_DIR, "TextClassfy/x.txt"), x)
        y = ReadFile(os.path.join(BASE_DIR, "TextClassfy/y.txt"), y)
        code = ReadFile(os.path.join(BASE_DIR, "TextClassfy/code.txt"), code)
        lx = len(x)
        Z = zeros(lx)
        Code = []
        for i in code:
            a = i.split(":")
            b = []
            for j in a:
                b.append(double(j))
            Code.append(b)
        rec = Record.objects.all()
        Name = []
        DName = {}
        for i in rec.all():
            if i.name != "":
                Name.append(i.name)
                for j in range(len(y)):
                    if i.name == y[j]:
                        Z += Code[j]
                        break
        for i in Name:
            DName.update({i: Name.count(i)})
        D1 = []
        D2 = []
        for k, v in DName.items():
            D1.append(k)
            D2.append(v)
        legend = ""
        for i in x:
            legend = legend + i + ","
        series = ""
        for i in Z:
            series = series + str(i) + ","
        response = HttpResponse(json.dumps({"legend":legend,"series":series,"D1":D1,"D2":D2}))
    except Exception as e:
        print(e)
        response = HttpResponse("SYSTEM ERROR")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def TextCNN(request):
    try:
        """
        socket
        """
        import socket
        CNNServerIP = "172.19.71.150"  # localhost
        CNNServerPoint = 8087
        obj = socket.socket()
        obj.connect((CNNServerIP, CNNServerPoint))
        x = []
        y = []
        x = ReadFile(os.path.join(BASE_DIR, "TextClassfy/x.txt"), x)
        y = ReadFile(os.path.join(BASE_DIR, "TextClassfy/y.txt"), y)
        lx = len(x)
        Z = zeros(lx)
        ONEHOT = eye(lx, dtype=float)
        rec = Record.objects.all()
        Name = []
        DName = {}
        for i in rec.all():
            if i.name != "":
                Name.append(i.name)
                obj.sendall(bytes(i.name, encoding="utf-8"))
                ret_bytes = obj.recv(1024)
                ret_str = str(ret_bytes, encoding="utf-8")
                for j in range(len(x)):
                    if ret_str == x[j]:
                        Z += ONEHOT[j]
                        break
        obj.sendall(bytes('end', encoding="utf-8"))
        obj.close()
        for i in Name:
            DName.update({i: Name.count(i)})
        D1 = []
        D2 = []
        for k, v in DName.items():
            D1.append(k)
            D2.append(v)
        legend = ""
        for i in x:
            legend = legend + i + ","
        series = ""
        for i in Z:
            series = series + str(i) + ","
        response = HttpResponse(json.dumps({"legend":legend,"series":series,"D1":D1,"D2":D2}))
    except Exception as e:
        print(e)
        response = HttpResponse("SYSTEM ERROR")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response
