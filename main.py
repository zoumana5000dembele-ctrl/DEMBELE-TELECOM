
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
import re

from src.usecases.list_tickets_categories import ListTicketsCategoriesUseCase

app = Flask(__name__)


@app.post('/payment')
def handle_payment():
    try:
        data = request.json
        sms_content = data.get('sms', 'Pas de SMS')

        price_match = re.search(r"(\d+)\s*FCFA", sms_content)
        telephone_match = re.search(r"du\s+([0-9*]+)", sms_content)
        transaction_id_match = re.search(r"ID:\s*([A-Z0-9.*]+)", sms_content)

        montant = price_match.group(1) if price_match else None
        telephone = telephone_match.group(1) if telephone_match else None
        transaction_id = transaction_id_match.group(
            1) if transaction_id_match else None

        message = (
            f"💰 **NOUVEAU PAIEMENT REÇU**\n\n"
            f"📞 **Téléphone :** {telephone}\n"
            f"🎫 **Forfait :** {montant}\n"
            f"🎫 **ID :** {transaction_id}\n"
            f"📱 **SMS :** `{sms_content}`\n\n"
            f"Vérifiez votre compte Orange Money, puis validez :"
        )

        print("MESSAGE TO SEND:", message)

        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.get("/")
def index():
    categories = ListTicketsCategoriesUseCase().execute()
    return render_template("index.html", categories=categories)


@app.get("/crud-tickets")
def crud_tickets():
    return render_template("crud-tickets.html")


@app.get("/consulter-temps-restants/<ticket_number>")
def consulter_temps_restants(ticket_number: str):
    return render_template("consulter-temps-restant.html", ticket_number=ticket_number)


if __name__ == "__main__":
    load_dotenv(".env")
    app.run(host='0.0.0.0', port=5000, debug=True)
