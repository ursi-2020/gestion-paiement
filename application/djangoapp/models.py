from django.db import models
from datetime import datetime

class Article(models.Model):
    nom = models.CharField(max_length=200)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return 'Article: {}'.format(self.nom)


class Vente(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return 'Vente: {} - {}'.format(self.article.nom, self.date)


class Produit(models.Model):
    codeProduit = models.CharField(max_length=200)
    familleProduit = models.CharField(max_length=200)
    descriptionProduit = models.CharField(max_length=200)
    quantiteMin = models.PositiveIntegerField()
    packaging = models.PositiveIntegerField()
    prix = models.PositiveIntegerField()

    def __str__(self):
        return "{\"codeProduit\":{}, \"familleProduit\":{}, \"descriptionProduit\":{},\"quantiteMin\":{}, \"packaging\":{}, \"prix\":{}}".format(self.codeProduit, self.familleProduit, self.descriptionProduit, self.quantiteMin, self.packaging, self.prix)


class Customer(models.Model):
    idClient = models.TextField(blank=False)
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    fidelityPoint = models.IntegerField(default=0)
    payment = models.IntegerField(default=0)
    account = models.CharField(max_length=10, default="")


class Transaction(models.Model):
    client_id = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return 'Transaction: {}'.format(self.date)


class Incident(models.Model):
    client_id = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=datetime.now, blank=True)
    message = models.CharField(max_length=255, default="")

    def __str__(self):
        return 'Incident: {}'.format(self.date)