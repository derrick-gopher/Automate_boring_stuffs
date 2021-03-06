from django.shortcuts import render
from .forms import UploadForm,VerifyFarmer
from django.http import HttpResponseRedirect
from .farmdrive import whitelist_f,verify_f
from django.http import JsonResponse,HttpResponse
import json
import re
import ast
from multiprocessing.pool import ThreadPool
# Create your views here.
def home(request):
    return render(request, 'home.html')

def index(request):
    form = UploadForm()
    vform = VerifyFarmer()
    return render(request, "index.html", {"form": form,"vform": vform})

def myajaxformview(request):
    if request.method == 'POST':
        if request.is_ajax():
            phone = request.POST.get("number", None)
            res = verify_f(phone)
            return HttpResponse(res)
    return render(request)



def whitelist(request):
    if request.method == 'POST':
        if request.is_ajax():
            number = request.POST.get("number", None)
            location = request.POST.get("location", None)
            match = re.findall(r'\d{9,12}', number)
            if match:
                nums254 = [x for x in match if x[0:3] == "254"]
                nums07 = ["254"+x[1:] for x in match if x[0] == "0"]
                nums7 = ["254"+x for x in match if x[0] == "7"]
                mylist = nums254+nums07+nums7
                chunk = 50
                a=[];b=[];c=0;w=[]
                if len(mylist) > chunk:
                    chunkedlist = [mylist[i:i+chunk] for i in range(len(mylist))[::chunk]]
                    newlist=[]
                    try:
                        for x in chunkedlist:
                            d = ",".join(x)
                            res = whitelist_f(d,location)
                            cd = json.loads(res)
                            a += cd["failed_numbers"]
                            b += cd["ignored_numbers"]
                            c += cd["total_submissions"]
                            w += cd["whitelisted_numbers"]
                        return HttpResponse(json.dumps({
                                "pass":1,
                                "failed_numbers":a,
                                "ignored_numbers":b,
                                "total_submissions":c,
                                "whitelisted_numbers":w
                            }))
                    except Exception as e:
                        return HttpResponse(json.dumps({"pass":0}))
                    
                else:
                    d = ",".join(mylist)
                    try:
                        res = whitelist_f(d,location)
                        cd = json.loads(res)
                        a += cd["failed_numbers"]
                        b += cd["ignored_numbers"]
                        c += cd["total_submissions"]
                        w += cd["whitelisted_numbers"]
                        return HttpResponse(json.dumps({
                                "pass":1,
                                "failed_numbers":a,
                                "ignored_numbers":b,
                                "total_submissions":c,
                                "whitelisted_numbers":w
                            }))
                    except Exception as e:
                        return HttpResponse(json.dumps({"pass":0}))
            else:
                #no match
                return HttpResponse(json.dumps({"pass":0}))
                    
    return render(request)
