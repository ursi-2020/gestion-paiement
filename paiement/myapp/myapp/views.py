from apipkg import api_manager as api
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

def index(request):
    time = api.send_request('scheduler', 'clock/time')
    return HttpResponse("L'heure de la clock est %r" % time)

def info(request):
	return JsonResponse({
        'id':3,
        'app-name':"Gestion Paiement",
        'desc':"Récupère les informations de paiement du client et renvoie si le paiement à réussi ou échoué. "
               "Stock également les historiques de paiement"
    })

def home(request):
    return render(request, 'core/home.html', {'user': "user"})