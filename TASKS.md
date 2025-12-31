## Spec

- En tant que client,
- Je veux pouvoir envoyer un message texte contenant les informations de paiement,
- Afin de recevoir mon ticket pour me connecter au Reseau


- En tant quer propriétaire,
- Je veux recevoir etre notifier de toutes les nouvelles demandes qui arrivent
- Afin de justement soit "Valider" ou "Refuser" l'access au reseaux



# Notes:
    Le proprietaire doit etre notifier par email (c'est le plus simple)
    La notification, designe un message text, avec un bouton qui lui redirige sur une page sur laquelle il va soit "Valider" ou "Refuser" la demande



### Exemple de message de paiement:
```Vous avez recu un transfert de 3300 FCFA du 79531543. ID: PP251226.2111.C98322. Consultez votre nouveau solde sur Max it ou au #144#6#. OFM MALI```




Discus avec ChatGpt

🔹 Cas le plus courant : ajouter un appareil via DHCP (recommandé)
    - PUT /rest/ip/dhcp-server/lease
            - body: {
                    "address": "192.168.1.50",
                    "mac-address": "AA:BB:CC:DD:EE:FF",
                    "server": "dhcp1",
                    "comment": "Téléphone bureau"
                }


exemple curl:
    curl -k -u admin:password \
  -X PUT https://192.168.88.1/rest/ip/dhcp-server/lease \
  -H "Content-Type: application/json" \
  -d '{
    "address": "192.168.88.50",
    "mac-address": "DC:A6:32:12:34:56",
    "server": "dhcp1",
    "comment": "PC Bureau Moussa"
  }'
