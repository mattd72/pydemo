import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
import datetime
from django.http import JsonResponse
from operator import itemgetter


def test(request):
    return HttpResponse("Testing...")

def dt(request):
    now = datetime.datetime.now()
    html = "<html><body>%s</body></html>" % now
    return HttpResponse(html)

def index(request):
    return render(request, 'index.html', {'name': settings.PROJECT_NAME })

def env(request):
    ret_dict = {
                "draw": 1,
                "recordsTotal": 0,
                "recordsFiltered": 0,
                "data": []
                }
    
    for key, value in os.environ.items():
        ret_dict['data'].append((key, value))
        ret_dict['recordsTotal'] += 1
    
    ret_dict['data'] = sorted(ret_dict['data'])
    
    return JsonResponse(ret_dict)


def proc(request):
    ret_dict = {
                "draw": 1,
                "recordsTotal": 0,
                "recordsFiltered": 0,
                "data": []
                }
    
    processoutput = os.popen("ps -Af").read()
    for proc in processoutput.split('\n')[1:]:
        output = proc.split()
        if output:
            name = output[7].split('/')[-1]
            if ']' in name:
                continue
            line = (name[:30], output[0], output[1], output[2], " ".join(output[8:]))
            ret_dict['data'].append(line)
            ret_dict['recordsTotal'] += 1
    
    ret_dict['data'] = sorted(ret_dict['data'],key=itemgetter(1))
    
    return JsonResponse(ret_dict)



