from django.http import HttpResponse
from apipkg import api_manager as api
from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
from . import models
from .forms import NameForm

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
    form = NameForm()
    info = json.loads(api.send_request('gestion-paiement', 'info'))
    transactions = json.loads(json.loads(api.send_request('gestion-paiement', 'transactions')))
    products = json.loads(json.loads(api.send_request('gestion-paiement', 'products')))
    return render(request, 'home.html', {'info': info, 'form': form, 'transactions': transactions, 'products': products})

def transactions(request):
    transactions = serializers.serialize('json', models.Transaction.objects.all())
    return JsonResponse(transactions, safe=False)

def products(request):
    products = serializers.serialize('json', models.Produit.objects.all())
    return JsonResponse(products, safe=False)

# Main function that handles paiement
@csrf_exempt
def proceed_payement(request):
    if request.method != 'POST':
        return HttpResponse("Forbidden")
    else:
        models.Transaction.objects.create(amount=request.POST['amount'])
        return HttpResponse("Saved")

# Import Catalogue Produit
@csrf_exempt
def load_product_catalogue(request):
    if request.method != 'POST':
        return HttpResponse("Forbidden")
    else:
        models.Produit.objects.all().delete()
        data = api.send_request("catalogue-produit", "api/data")
        json_data = json.loads(data)
        for product in json_data["produits"]:
            produits = models.Produit(codeProduit=product["codeProduit"],
                                      familleProduit=product["familleProduit"],
                                      descriptionProduit=product["descriptionProduit"],
                                      quantiteMin=product["quantiteMin"] , packaging=product["packaging"], prix=product["prix"])
            produits.save()
        return HttpResponse("Success")