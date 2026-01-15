
import os
from typing import Any, Dict
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, Response
import re

from asgiref.wsgi import WsgiToAsgi

from src.usecases.list_tickets_categories import ListTicketsCategoriesUseCase
from src.usecases.add_tickets import AddTicketsCommand, AddTicketsUseCase
from src.usecases.create_ticket_request import CreateTicketRequestCommand, CreateTicketRequestUseCase
from src.usecases.validate_ticket_request import ValidateTicketRequestUseCase
from src.usecases.refuse_ticket_request import RefuseTicketRequestUseCase
from src.usecases.list_ticket_requests import ListTicketRequestsUseCase
from src.usecases.get_ticket_request_status import GetTicketRequestStatusUseCase
from src.http.dto import TicketRequestDTO, TicketRequestStatusDTO
from src.db.models import RequestStatus
from src.services.email_service import send_admin_notification_email


app = Flask(__name__)
asgi_app = WsgiToAsgi(app)

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


@app.get("/")
def root():
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


@app.post("/api/create-ticket-request")
def create_ticket_request():
    try:
        data: Dict[str, Any] = request.json
        if not data:
            return jsonify({"status": "error", "message": "Body missing"}), 400

        category_id = data.get("category_id")
        client_name = data.get("client_name")
        client_phone = data.get("client_phone")
        sms_content = data.get("sms_content")

        if not category_id or not client_name or not client_phone:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        use_case = CreateTicketRequestUseCase()
        command = CreateTicketRequestCommand(
            category_id=category_id,
            client_name=client_name,
            client_phone=client_phone,
            sms_content=sms_content,
        )

        request_entity = use_case.execute(command)

        # Envoyer un email à l'administrateur
        try:
            send_admin_notification_email(
                request_entity.id, client_name, client_phone, sms_content)
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email: {e}")

        return jsonify({
            "status": "ok",
            "request_id": request_entity.id,
            "message": "Votre demande a été envoyée. Vous recevrez une notification une fois validée."
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.get("/api/ticket-request/<request_id>")
def get_ticket_request_status(request_id: str):
    try:
        use_case = GetTicketRequestStatusUseCase()
        request_model = use_case.execute(request_id)

        if not request_model:
            return jsonify({"status": "error", "message": "Request not found"}), 404

        dto = TicketRequestStatusDTO(
            id=request_model.id,
            status=request_model.status.value,
            category_name=request_model.category.name if request_model.category else "",
            category_price=request_model.category.price if request_model.category else "",
            created_at=request_model.created_at,
            client_phone=request_model.client_phone,
            ticket_access_key=request_model.ticket.access_key if request_model.ticket else None,
        )

        return jsonify({
            "status": "ok",
            "request": {
                "id": dto.id,
                "status": dto.status,
                "category_name": dto.category_name,
                "category_price": dto.category_price,
                "created_at": dto.created_at.isoformat(),
                "client_phone": dto.client_phone,
                "ticket_access_key": dto.ticket_access_key,
            }
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.get("/request/<request_id>")
def request_status_page(request_id: str):
    return render_template("request-status.html", request_id=request_id)


@app.get("/api/admin/ticket-requests")
def list_ticket_requests():
    try:
        status_param = request.args.get("status", "pending")
        status = None
        if status_param == "pending":
            status = RequestStatus.PENDING
        elif status_param == "validated":
            status = RequestStatus.VALIDATED
        elif status_param == "refused":
            status = RequestStatus.REFUSED

        use_case = ListTicketRequestsUseCase()
        requests = use_case.execute(status)

        requests_dto: Any = []
        for req in requests:
            dto = TicketRequestDTO(
                id=req.id,
                category_id=req.category_id,
                category_name=req.category.name if req.category else "",
                category_price=req.category.price if req.category else "",
                client_name=req.client_name,
                client_phone=req.client_phone,
                sms_content=req.sms_content,
                status=req.status.value,
                created_at=req.created_at,
                validated_at=req.validated_at,
                ticket_access_key=req.ticket.access_key if req.ticket else None,
            )
            requests_dto.append({
                "id": dto.id,
                "category_id": dto.category_id,
                "category_name": dto.category_name,
                "category_price": dto.category_price,
                "client_name": dto.client_name,
                "client_phone": dto.client_phone,
                "sms_content": dto.sms_content,
                "status": dto.status,
                "created_at": dto.created_at.isoformat(),
                "validated_at": dto.validated_at.isoformat() if dto.validated_at else None,
                "ticket_access_key": dto.ticket_access_key,
            })

        return jsonify({"status": "ok", "requests": requests_dto}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.post("/api/admin/validate-request/<request_id>")
def validate_request(request_id: str):
    try:
        use_case = ValidateTicketRequestUseCase()
        request_model = use_case.execute(request_id)

        if not request_model:
            return jsonify({"status": "error", "message": "Request not found or already processed"}), 404

        return jsonify({
            "status": "ok",
            "message": "Request validated successfully",
            "ticket_access_key": request_model.ticket.access_key if request_model.ticket else None,
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.post("/api/admin/refuse-request/<request_id>")
def refuse_request(request_id: str):
    try:
        use_case = RefuseTicketRequestUseCase()
        request_model = use_case.execute(request_id)

        if not request_model:
            return jsonify({"status": "error", "message": "Request not found or already processed"}), 404

        return jsonify({
            "status": "ok",
            "message": "Request refused successfully",
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


PORT = int(os.getenv("PORT", "8000"))
DEBUG = bool(int(os.getenv("DEBUG", "1")))

if __name__ == "__main__":
    load_dotenv(".env")
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
