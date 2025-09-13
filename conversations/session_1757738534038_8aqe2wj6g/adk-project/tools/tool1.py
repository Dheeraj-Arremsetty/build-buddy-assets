from flask import Flask, jsonify, request
import datetime

app = Flask(__name__)

# Mock S&P Financials API Data
mock_financial_data = {
    "QLI": { "companyName": "QuantumLeap Inc.", "ticker": "QLI", "marketCap": "950B USD", "peRatio": 35.2, "eps": 8.75, "52WeekHigh": 350.12, "52WeekLow": 210.45, "analystRating": "Strong Buy" },
    "AUTX": { "companyName": "AutoNoma GMBH", "ticker": "AUTX", "marketCap": "450B EUR", "peRatio": 18.5, "eps": 4.20, "52WeekHigh": 150.80, "52WeekLow": 95.25, "analystRating": "Hold" },
    "SHIP": { "companyName": "Global Maritime Logistics", "ticker": "SHIP", "marketCap": "120B USD", "peRatio": 12.1, "eps": 2.50, "52WeekHigh": 75.00, "52WeekLow": 45.00, "analystRating": "Buy" },
    "RETL": { "companyName": "Worldwide Retail Corp", "ticker": "RETL", "marketCap": "300B USD", "peRatio": 22.8, "eps": 5.10, "52WeekHigh": 210.00, "52WeekLow": 150.00, "analystRating": "Hold" }
}

# Mock Sector Performance API Data
mock_sector_data = {
    "Semiconductors": { "sector": "Semiconductors", "ytdPerformance": "+22.5%", "dailyChange": "+1.8%", "keyDrivers": ["AI demand", "Data center growth"], "outlook": "Positive" },
    "Automotive": { "sector": "European Automotive", "ytdPerformance": "-5.2%", "dailyChange": "-2.1%", "keyDrivers": ["EV transition", "Trade tariffs", "Supply chain costs"], "outlook": "Neutral to Negative" },
    "Shipping": { "sector": "Global Shipping", "ytdPerformance": "+8.0%", "dailyChange": "-3.5%", "keyDrivers": ["Global trade volume", "Fuel costs", "Port congestion"], "outlook": "Volatile" }
}

# Mock News Feed API Data
mock_news_data = {
    "quantumleap inc.": [
        { "headline": "QuantumLeap Inc. Unveils Fusion-Powered Processor, Stock Soars 30%", "source": "TechCrunch", "timestamp": datetime.datetime.utcnow().isoformat() + "Z", "summary": "The tech giant announced a breakthrough in processor technology that promises to revolutionize computing." },
        { "headline": "Regulators to Scrutinize QuantumLeap's New Technology", "source": "Wall Street Journal", "timestamp": (datetime.datetime.utcnow() - datetime.timedelta(hours=1)).isoformat() + "Z", "summary": "Global regulatory bodies have expressed concerns over the potential monopolistic implications." }
    ],
    "trade tariffs": [
        { "headline": "New Trans-Atlantic Trade Tariffs Announced, Targeting Automotive and Luxury Goods", "source": "Reuters", "timestamp": datetime.datetime.utcnow().isoformat() + "Z", "summary": "Governments have imposed new tariffs, escalating trade tensions and rattling the European automotive industry." }
    ],
    "suez canal blockage": [
        { "headline": "BREAKING: Container Ship Blocks Suez Canal, Global Shipping Grinds to a Halt", "source": "Associated Press", "timestamp": datetime.datetime.utcnow().isoformat() + "Z", "summary": "A massive container ship has become wedged across the Suez Canal, causing a major traffic jam of vessels." }
    ]
}

@app.route('/financials/<ticker>', methods=['GET'])
def get_financials(ticker):
    data = mock_financial_data.get(ticker.upper())
    if data: return jsonify(data)
    return jsonify({"error": "Ticker not found"}), 404

@app.route('/sector/<sector_name>', methods=['GET'])
def get_sector_performance(sector_name):
    for key, value in mock_sector_data.items():
        if sector_name.lower() in key.lower():
            return jsonify(value)
    return jsonify({"error": "Sector not found"}), 404

@app.route('/news', methods=['GET'])
def get_news():
    query = request.args.get('q', '').lower()
    for key, articles in mock_news_data.items():
        if query in key:
            return jsonify({"articles": articles})
    return jsonify({"articles": []})

if __name__ == '__main__':
    app.run(port=5001, debug=True)