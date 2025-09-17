import json
from flask import Flask, jsonify, request

app = Flask(__name__)

# Realistic synthetic customer data
mock_db = {
    "Global Tech Inc.": {
        "id": "acc001",
        "name": "Global Tech Inc.",
        "contactPerson": "Jane Doe",
        "address": "123 Tech Park, Silicon Valley, CA 94001",
        "industry": "Technology",
    },
    "Innovate Solutions": {
        "id": "acc002",
        "name": "Innovate Solutions",
        "contactPerson": "John Smith",
        "address": "456 Innovation Dr, Boston, MA 02101",
        "industry": "Consulting",
    },
    "Creative Designs": {
        "id": "acc003",
        "name": "Creative Designs",
        "contactPerson": "Emily White",
        "address": "789 Art Ave, New York, NY 10001",
        "industry": "Marketing",
    }
}

mock_history = {
    "acc001": [
        {"date": "2024-05-20", "activity": "Closed Won - Printer Fleet Upgrade", "amount": 75000},
        {"date": "2024-02-10", "activity": "Support Ticket #4521 Resolved", "amount": 0}
    ],
    "acc002": [
        {"date": "2024-06-01", "activity": "Initial Consultation - IT Services", "amount": 0}
    ],
    "acc003": [
         {"date": "2023-11-15", "activity": "Contract Signed - Marketing Automation", "amount": 50000}
    ]
}

@app.route('/customers', methods=['GET'])
def get_customer_details():
    customer_name = request.args.get('name')
    if not customer_name:
        return jsonify({"error": "Customer name is required"}), 400
    
    customer_data = mock_db.get(customer_name)
    
    if customer_data:
        return jsonify(customer_data)
    else:
        return jsonify({"error": f"Customer '{customer_name}' not found"}), 404

@app.route('/history', methods=['GET'])
def get_account_history():
    customer_name = request.args.get('name')
    if not customer_name:
        return jsonify({"error": "Customer name is required"}), 400
    
    customer_data = mock_db.get(customer_name)
    if not customer_data:
        return jsonify({"error": f"Customer '{customer_name}' not found"}), 404
        
    account_id = customer_data.get('id')
    history = mock_history.get(account_id, [])
    
    return jsonify({"history": history})

if __name__ == '__main__':
    # Run on port 5003 to avoid conflicts with Orchestrate services
    app.run(port=5003, debug=True)