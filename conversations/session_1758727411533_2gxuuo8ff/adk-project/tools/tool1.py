from flask import Flask, jsonify

app = Flask(__name__)

# Synthetic inventory database
INVENTORY_DB = {
    "HG-455B": {
        "part_number": "HG-455B",
        "description": "Main gear axle nut",
        "quantity": 12,
        "location": "ATL-Hangar 3",
        "last_updated": "2024-10-21T14:30:00Z"
    },
    "BRK-PIN-991": {
        "part_number": "BRK-PIN-991",
        "description": "Brake wear indicator pin",
        "quantity": 150,
        "location": "ATL-Hangar 2",
        "last_updated": "2024-10-20T11:00:00Z"
    },
    "B-UNIT-78C": {
        "part_number": "B-UNIT-78C",
        "description": "Brake unit assembly",
        "quantity": 4,
        "location": "DFW-Central Stores",
        "last_updated": "2024-10-21T09:15:00Z"
    }
}

@app.route('/inventory/<string:part_number>', methods=['GET'])
def get_inventory(part_number):
    """Endpoint to get inventory details for a specific part number."""
    part_details = INVENTORY_DB.get(part_number.upper())
    if part_details:
        return jsonify(part_details)
    else:
        return jsonify({"error": "Part not found"}), 404

if __name__ == '__main__':
    # Run the API on localhost port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)