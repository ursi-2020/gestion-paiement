from django.http import HttpResponse
from apipkg import api_manager as api
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
import json

from pip._vendor import requests

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

def clean_transactions(request):
    models.Transaction.objects.all().delete()
    return redirect(ihm)

def clean_incidents(request):
    models.Incident.objects.all().delete()
    return redirect(ihm)

# Main function that handles paiement
@csrf_exempt
def proceed_payement(request):
    if request.method != 'POST':
        return HttpResponse(status=403)
    else:
        today = api.send_request('scheduler', 'clock/time')
        time = datetime.strptime(today, '"%d/%m/%Y-%H:%M:%S"')
        client_id = request.POST.get('client_id')
        card = request.POST.get('card', None)
        amount = request.POST.get('amount')
        payement_method = request.POST.get('payement_method')
        credit_date = request.POST.get('credit_date')

        if payement_method == 'CREDIT':
            if not credit_date:
                return JsonResponse({
                    'status': 'ERROR',
                    'message': 'Transaction refusée! Pas date de credit entrée.'
                })
            body = {'idClient': client_id, 'Montant': amount, 'Date': credit_date}
            status_res = api.post_request2('crm', '/api/allow_credit', json.dumps(body))
            if status_res != None:
                data = json.loads(status_res[1].content.decode('utf-8'))
                print("Data", data)
                if data['Allowed']:
                    return JsonResponse({
                        'status': 'OK',
                        'message': 'Transaction acceptée!'
                    })
                else:
                    return JsonResponse({
                        'status': 'ERROR',
                        'message': 'Transaction refusée, client non authorisé.'
                    })
            return JsonResponse({
                'status': 'ERROR',
                'message': 'Transaction refusée, client inconnu au bataillon.'
            })
        elif payement_method == 'CASH':
            return JsonResponse({
                'status': 'OK',
                'message': 'Transaction inutile sur du cash.'
            })

        if randint(0,3) == 0:
            message = 'Cause possible: random.'
            models.Incident.objects.create(client_id=client_id, amount=amount, date=time, message=message)
            return JsonResponse({
                'status': 'ERROR',
                'message': 'Transaction refusée! ' + message
            })
        else:
            models.Transaction.objects.create(client_id=client_id, amount=amount, date=time)
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
            client_tmp = models.Customer(idClient=client["IdClient"],
                                      firstName=client["Prenom"],
                                      lastName=client["Nom"],
                                      fidelityPoint=client["Credit"],
                                        payment=client["Montant"], account=client["Compte"])
            client_tmp.save()
        return HttpResponse("Clients sauvegardés.")


@csrf_exempt
def schedule_load_clients(request):
    clock_time = api.send_request('scheduler', 'clock/time')
    time = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    time = time + timedelta(seconds=180)
    time_str = time.strftime('%d/%m/%Y-%H:%M:%S')
    body = {
        "target_app": 'gestion-paiement',
        "target_url": '/load-clients',
        "time": time_str,
        "recurrence": "day",
        "data": '{}',
        "source_app": "gestion-paiement",
        "name": "gestion-paiement-load-clients"
    }
    schedule_task(body)
    return redirect('index')


def schedule_task(body):
    headers = {'Host': 'scheduler'}
    r = requests.post(api.api_services_url + 'schedule/add', headers=headers, json=body)
    print("schedule error code: ")
    print(r.status_code)
    print(r.text)
    return
