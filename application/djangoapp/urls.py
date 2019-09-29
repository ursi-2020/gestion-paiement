from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('info', views.info, name='info'),
    path('ihm', views.ihm, name='ihm'),
    path('proceed-payement', views.proceed_payement, name='proceed-payement'),
    path('transactions', views.transactions, name='transactions'),
    path('products', views.products, name='products'),
    path('load-products', views.load_product_catalogue, name='load-products'),
]