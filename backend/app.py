from flask import Flask, request, jsonify, send_from_directory
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
        report_id = str(uuid.uuid4())  # Creating the id of the form and report
        data["id"] = report_id 
        data["creation_date"] = datetime.now().isoformat()  
        pdf_filename = f"report_{data['id']}.pdf"
        data["report_url"] = os.path.join(REPORTS_PATH, pdf_filename)
        data["report_data"] = generate_report(data, os.path.join(REPORTS_PATH, pdf_filename))

        with open(DATA_PATH, 'r+') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
            existing_data.append(data)
            f.seek(0)
            json.dump(existing_data, f, indent=4)


        return jsonify({"message": "Data saved successfully!", "report_id": report_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@app.route('/forms', methods=['GET'])
def get_all_forms():
    try:
        with open(DATA_PATH, 'r') as f:
            forms = json.load(f)
        return jsonify(forms), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/reports/<path:filename>', methods=['GET'])
def serve_report(filename):
    try:
        return send_from_directory(REPORTS_PATH, filename, as_attachment=False)
    except Exception as e:
        return jsonify({"error": str(e)}), 404
    

@app.route('/get_report_data', methods=['GET'])
def get_report_data():
    try:
        report_id = request.args.get('report_id')
        
        with open(DATA_PATH, 'r') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
        
        report = next((item for item in existing_data if item['id'] == report_id), None)
        
        if report:
            return jsonify(report['report_data']), 200
        else:
            return jsonify({"error": "Report not found"}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)