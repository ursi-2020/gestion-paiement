[Sommaire](https://ursi-2020.github.io/Documentation/)
    
# Gestion Paiement API

####Procéder au paiement
* route: 'api/proceed-payement'
* body: {
<br>client_id: l'id du client qui effectue le paiement
<br>payement_method: la méthode de paiement ('CARD' ou 'CASH')
<br>card: le numéro de carte du client (requis si payement_method = 'CARD')
<br>amount (requis): le montant du paiement
<br>}
* retourne: {
<br>status: 'OK' ou 'ERROR'
<br>message: un commentaire sur le statut
<br>}

#### Récupérer les informations de transaction
* route: 'api/transactions'
* route: 'api/transactions?client_id='
* retourne: un tableau contenat toutes les transactions
ou celle d'un client si son ID est spécifié dans la requête