from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import base64, datetime

from apps.api.models import models

@csrf_exempt
def signup(request):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        email = request.POST.get('email')
        pw = request.POST.get('pw')
        type = request.POST.get('type')

        if email and pw and type:
            models.User.objects.create(
                email = email,
                pw = pw,
                type = type
            )
        else:
            return HttpResponse(status=400) # Bad Request

    return HttpResponse(status=200)


def list(request):
    if request.method == "GET":
        objects = models.Request.objects.all().order_by('-requested',)
        data = []
        for o in objects:
            data.append({
                "id" : o.id,
                "status" : o.status,
                "from_addr" : o.from_addr,
                "to_addr" : o.to_addr,
                "user_id" : o.user_id,
                "driver_id" : o.driver_id,
                "requested" : o.requested,
                "assigned" : o.assigned,
            })

    elif request.method == "POST":
        pass
    return JsonResponse({'data': data})


@csrf_exempt
def allocation(request):
    auth = request.headers.get('Authorization')
    if auth:
        auths = auth.split()
        if auths[0] == 'Basic':
            authstring = base64.b64decode(auths[1]).decode("UTF-8")
            email = (authstring.split(":"))[0]
            pw = (authstring.split(":"))[1]
            user = models.User.objects.filter(email = email
            ).filter(
                pw = pw
            )
            if len(user) == 1:
                pass
            else: 
                return HttpResponse(status=403) # 403 Forbidden
        else:
            return HttpResponse(status=401) # Unauthorized
    else:
        return HttpResponse(status=401) # Unauthorized


    if request.method == "GET":
        pass
    elif request.method == "POST":
        from_addr = request.POST.get("from_addr")
        to_addr = request.POST.get("to_addr")

        if from_addr and to_addr:
            models.Request.objects.create(
                status = "INIT",
                from_addr = from_addr,
                to_addr = to_addr,
                user_id = user[0].id,
            )
        else:
            return HttpResponse(status=400) # Bad Request
        
    return HttpResponse() # 200 OK


@csrf_exempt
def assignment(request):
    auth = request.headers.get('Authorization')
    if auth:
        auths = auth.split()
        if auths[0] == 'Basic':
            authstring = base64.b64decode(auths[1]).decode("UTF-8")
            email = (authstring.split(":"))[0]
            pw = (authstring.split(":"))[1]
            user = models.User.objects.filter(email = email
            ).filter(
                pw = pw
            )
            if len(user) == 1:
                pass
            else: 
                return HttpResponse(status=403) # 403 Forbidden
        else:
            return HttpResponse(status=401) # Unauthorized
    else:
        return HttpResponse(status=401) # Unauthorized

    if request.method == "GET":
        pass
    elif request.method == "POST":
        request_id = request.POST.get('request_id')
        if request_id:
            request = models.Request.objects.get(id = request_id)
            if request.status == 'INIT':
                request.driver_id = user[0].id
                request.assigned = datetime.datetime.utcnow()
                request.status = 'ASSG'
                request.save()
            else:
                return HttpResponse(status=400) # Bad Request
        else:
            return HttpResponse(status=400) # Bad Request
    return HttpResponse() # 200 OK