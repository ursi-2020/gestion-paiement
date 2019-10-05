from django.urls import path

from . import views

urlpatterns = [
    path('', views.ihm, name='index'),
    path('api/info', views.info, name='info'),
    path('api/proceed-payement', views.proceed_payement, name='proceed-payement'),
    path('api/transactions', views.transactions, name='transactions'),
    path('load-products', views.load_product_catalogue, name='load-products'),
    path('load-clients', views.load_clients, name='load-clients'),
]