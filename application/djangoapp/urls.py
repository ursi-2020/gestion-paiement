from django.urls import path

from . import views

urlpatterns = [
    path('', views.ihm, name='index'),
    path('info', views.info, name='info'),
    path('proceed-payement', views.proceed_payement, name='proceed-payement'),
    path('transactions', views.transactions, name='transactions'),
    path('products', views.products, name='products'),
    path('clients', views.clients, name='clients'),
    path('load-products', views.load_product_catalogue, name='load-products'),
    path('load-clients', views.load_clients, name='load-clients'),
]