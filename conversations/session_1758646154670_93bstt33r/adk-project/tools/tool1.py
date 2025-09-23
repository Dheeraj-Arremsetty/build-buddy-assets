# mock_sap_api.py
import json
from flask import Flask, request, jsonify
import datetime
import random

app = Flask(__name__)

@app.route('/invoices', methods=['POST'])
def create_invoice_entry():
    """
    Mock SAP API endpoint to create a payment entry.
    Accepts JSON invoice data and returns a transaction ID.
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    invoice_data = request.get_json()
    print(f"[Mock SAP API] Received data: {json.dumps(invoice_data, indent=2)}")

    # Basic validation
    required_fields = ["invoice_id", "vendor_name", "total_amount"]
    if not all(field in invoice_data for field in required_fields):
        return jsonify({"error": "Missing required fields in invoice data"}), 400

    # Generate a realistic, synthetic transaction ID
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = random.randint(1000, 9999)
    transaction_id = f"SAP-TRX-{timestamp}-{random_suffix}"

    print(f"[Mock SAP API] Successfully processed. Transaction ID: {transaction_id}")

    return jsonify({
        "status": "success",
        "message": "Invoice processed and scheduled for payment.",
        "transactionId": transaction_id
    }), 201

if __name__ == '__main__':
    # Run the app on localhost, port 5001 to avoid conflicts
    app.run(host='0.0.0.0', port=5001, debug=True)