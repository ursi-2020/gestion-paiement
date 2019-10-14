from django.http import HttpResponse
from apipkg import api_manager as api
from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
from . import models
from random import *

def index(request):
    time = api.send_request('scheduler', 'clock/time')
    return HttpResponse("L'heure de la clock est %r" % time)

# Informations about the app
def info(request):
    return JsonResponse({
        'id':"gestion-paiement",
        'name':"Gestion Paiement",
        'desc':"Récupère les informations de paiement du client et renvoie si le paiement à réussi ou échoué. "
               "Stock également les historiques de paiement."
    })

# The IHM for testing purpose
def ihm(request):
    info = json.loads(api.send_request('gestion-paiement', 'api/info'))
    context = {
        'info': info,
        'transactions': models.Transaction.objects.all(),
        'incidents': models.Incident.objects.all(),
        'products': models.Produit.objects.all(),
        'clients': models.Customer.objects.all()
    }
    return render(request, 'home.html', context)

def transactions(request):
    client_id = request.GET.get('client_id')
    if (client_id):
        transactions = list(models.Transaction.objects.filter(client_id=client_id).values())
        return JsonResponse(transactions, safe=False)
    else:
        transactions = list(models.Transaction.objects.all().values())
        return JsonResponse(transactions, safe=False)

# Main function that handles paiement
@csrf_exempt
def proceed_payement(request):
    if request.method != 'POST':
        return HttpResponse(status=403)
    else:
        client_id = request.POST.get('client_id')
        card = request.POST.get('card', None)
        amount = request.POST.get('amount')

        if randint(0,3) == 0:
            models.Incident.objects.create(client_id=client_id, amount=amount)
            return JsonResponse({
                'status': 'ERROR',
                'message': 'Transaction refusée! Cause possible: random'
            })
        else:
            models.Transaction.objects.create(client_id=client_id, amount=amount)
            return JsonResponse({
                'status': 'OK',
                'message': 'Transaction acceptée!'
            })

# Import Catalogue Produit
@csrf_exempt
def load_product_catalogue(request):
    if request.method != 'POST':
        return HttpResponse(status=403)
    else:
        models.Produit.objects.all().delete()
        data = api.send_request("catalogue-produit", "api/get-all")
        json_data = json.loads(data)
        for product in json_data["produits"]:
            produits = models.Produit(codeProduit=product["codeProduit"],
                                      familleProduit=product["familleProduit"],
                                      descriptionProduit=product["descriptionProduit"],
                                      quantiteMin=product["quantiteMin"] , packaging=product["packaging"], prix=product["prix"])
            produits.save()
        return HttpResponse("Produits sauvegardés.")

# Import Clients list
@csrf_exempt
def load_clients(request):
    if request.method != 'POST':
        return HttpResponse(status=403)
    else:
        models.Customer.objects.all().delete()
        data = api.send_request("crm", "api/data")
        json_data = json.loads(data)
        for client in json_data:
            client_tmp = models.Customer(idClient=client["idClient"],
                                      firstName=client["firstName"],
                                      lastName=client["lastName"],
                                      fidelityPoint=client["fidelityPoint"] ,
                                        payment=client["payment"], account=client["account"])
            client_tmp.save()
        return HttpResponse("Clients sauvegardés.")