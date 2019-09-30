[Sommaire](https://ursi-2020.github.io/Documentation/)
    
# Gestion Paiement API

### Procéder au paiement

* route: 'proceed-paiement'
* body: amount=decimal (mandatory)
* retourne: 'Success' si transaction réussi, une erreur sinon

### Récupérer les informations de transaction

* route: 'transactions'
* retourne: toute les transactions