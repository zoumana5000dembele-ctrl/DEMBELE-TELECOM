
from typing import Any, Dict
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, Response
import re

from src.usecases.list_tickets_categories import ListTicketsCategoriesUseCase
from src.usecases.add_tickets import AddTicketsCommand, AddTicketsUseCase

app = Flask(__name__)

TICKET_ACCESS_KEYS_SEPARATOR = ","


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


@app.get("/checkout")
def checkout():
    categories = ListTicketsCategoriesUseCase().execute()
    return render_template("checkout.html", categories=categories)


@app.get("/dashboard")
def dashboard():
    categories = ListTicketsCategoriesUseCase().execute()
    return render_template("dashboard.html", categories=categories)


@app.post("/api/add-tickets")
def add_tickets():
    data: Dict[str, Any] = request.json

    if not data:
        return Response("Body missing", status=500)

    ticket_access_keys: str | None = data.get("ticket_access_keys", None)
    category_id: str | None = data.get("ticket_category_id", None)
    if not ticket_access_keys or not category_id:
        return Response("Missing params", status=400)

    add_tickets_use_case = AddTicketsUseCase()
    command = AddTicketsCommand(
        access_keys=[
            access_key.strip()
            for access_key in ticket_access_keys.split(TICKET_ACCESS_KEYS_SEPARATOR)
            if access_key.strip()
        ],
        category_id=category_id
    )

    tickets = add_tickets_use_case.execute(command)

    return jsonify({"status": "ok", "tickets": len(tickets)}), 200


@app.get("/consulter-temps-restants/<ticket_number>")
def consulter_temps_restants(ticket_number: str):
    return render_template("consulter-temps-restant.html", ticket_number=ticket_number)


if __name__ == "__main__":
    load_dotenv(".env")
    app.run(host='0.0.0.0', port=5000, debug=True)
