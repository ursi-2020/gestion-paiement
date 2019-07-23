from django.http import HttpResponse
from apipkg import api_manager as api
from django.http import JsonResponse
from django.shortcuts import render
import json

def index(request):
    time = api.send_request('scheduler', 'clock/time')
    return HttpResponse("L'heure de la clock est %r" % time)

def info(request):
    if request.method != "GET":
        return HttpResponse("Forbidden")
    else:
        return JsonResponse({
            'id':3,
            'app_name':"Gestion Paiement",
            'desc':"Récupère les informations de paiement du client et renvoie si le paiement à réussi ou échoué. "
                   "Stock également les historiques de paiement"
        })

def ihm(request):
    if request.method != "GET":
        return HttpResponse("Forbidden")
    else:
        paiement_info = json.loads(api.send_request('gestion-paiement', 'info'))
        ecommerce_info = api.send_request('e-commerce', 'ecommerce/hello')
        #print = api.post_request('e-commerce', 'ecommerce/print', '{"app_name": "gestion-paiement", "message": "Hello"}')
        return render(request, 'home.html', {'app_a': paiement_info, 'app_b': ecommerce_info})

def paiement(request):
    if request.method != 'POST':
        return HttpResponse("Forbidden")
    else:
        jsonBody = json.loads(request.body)
        return HttpResponse(jsonBody["app_name"] + " : " + jsonBody["message"])