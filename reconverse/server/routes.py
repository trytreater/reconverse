from datetime import datetime
from flask import request, jsonify

def configure_routes(server, api):
    @api.route('/')
    def home():
        return "Welcome to Reconverse."

    @api.route('/internalize', methods=['POST'])
    def internalize():
        # Extract and validate JSON request data
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON body required"}), 400

        raw_text = data.get("raw_text")
        document_type = data.get("document_type")
        counterparty_id = data.get("counterparty_id")
        expects_response = data.get("expects_response", False)

        # Validate fields
        if not isinstance(raw_text, str):
            return jsonify({"error": "raw_text must be a string"}), 400
        if not isinstance(document_type, str):
            return jsonify({"error": "document_type must be a string"}), 400
        if document_type not in server.accepted_document_types:
            return jsonify({f"error": f"document_type {document_type} not accepted. \n Accepted document types: {server.accepted_document_types}"}), 400
        if not isinstance(counterparty_id, str):
            return jsonify({"error": "counterparty_id must be a string"}), 400
        if not isinstance(expects_response, bool):
            return jsonify({"error": "expects_response must be a boolean"}), 400

        # Forward the data to the service layer for processing
        context = server.internalize(raw_text, document_type, counterparty_id, expects_response)

        context = "placeholder"

        now = datetime.now()
        response = {"Timestamp: ": now.isoformat(),
                    "Counterparty_ID": counterparty_id,
                    "expects_response": expects_response}
        if expects_response:
            response["context"] = context  # Include context if response is expected

        return jsonify(response), 200