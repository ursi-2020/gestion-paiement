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
               "Stock également les historiques de paiement"
    })

# The IHM for testing purpose
def ihm(request):
    form = NameForm()
    info = json.loads(api.send_request('gestion-paiement', 'gestion-paiement/info'))
    transactions = json.loads(json.loads(api.send_request('gestion-paiement', 'gestion-paiement/transaction')))
    return render(request, 'home.html', {'info': info, 'form': form, 'transactions': transactions})

def transactions(request):
    transactions = serializers.serialize('json', models.Transaction.objects.all())
    return JsonResponse(transactions, safe=False)

# Main function that handles paiement
@csrf_exempt
def proceed_payement(request):
    if request.method != 'POST':
        return HttpResponse("Forbidden")
    else:
        models.Transaction.objects.create(amount=request.POST['amount'])
        return HttpResponse("Saved")

# Import Catalogue Produit
def load_product_catalogue(request):
    data = api.send_request("catalogue-produit", "catalogueproduit/api/data")
    try:
        json_data = json.loads(data)

        for product in json_data["produits"]:
            produits = models.Produit(codeProduit=product["codeProduit"], quantiteMin=product["quantiteMin"],
                                      packaging=product["packaging"], prix=product["prix"])
            produits.save()
    except:
        print(data)

    products = serializers.serialize('json', models.Produit.objects.all())
    return JsonResponse(products, safe=False)