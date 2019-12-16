from django.urls import path

from . import views

urlpatterns = [
    path('', views.ihm, name='index'),
    path('', views.schedule_load_clients, name='auto_schedule_load_clients'),
    path('api/info', views.info, name='info'),
    path('api/proceed-payement', views.proceed_payement, name='proceed-payement'),
    path('api/transactions', views.transactions, name='transactions'),
    path('load-products', views.load_product_catalogue, name='load-products'),
    path('clean-transactions', views.clean_transactions, name='clean_transactions'),
    path('clean-incidents', views.clean_incidents, name='clean_incidents'),
    path('load-clients', views.load_clients, name='load-clients'),
    path('schedule_load_clients', views.schedule_load_clients, name='schedule_load_clients'),
]
