from flask import Flask, request, jsonify
import json
import os
import uuid
from datetime import datetime
from report_generator import generate_report 


app = Flask(__name__)  

DATA_PATH = "data/forms_data.json"
REPORTS_PATH = "reports/"

os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
os.makedirs(REPORTS_PATH, exist_ok=True)

# Endpoint to save form data
@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.json
    try:
        data["id"] = str(uuid.uuid4())  # Creating the id of the form adn report
        data["creation_date"] = datetime.now().isoformat()  
        pdf_filename = f"report_{data['id']}.pdf"
        data["report_url"] = os.path.join(REPORTS_PATH, pdf_filename)

        with open(DATA_PATH, 'r+') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
            existing_data.append(data)
            f.seek(0)
            json.dump(existing_data, f, indent=4)

        # Report
        generate_report(data, os.path.join(REPORTS_PATH, pdf_filename))

        return jsonify({"message": "Data saved and report generated successfully!", "report_url": data["report_url"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)