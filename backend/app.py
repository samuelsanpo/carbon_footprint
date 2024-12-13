from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)  

DATA_PATH = "data/forms_data.json"

os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)


# Endpoint to save form data
@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.json
    try:
        # Save data to JSON
        with open(DATA_PATH, 'r+') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
            existing_data.append(data)
            f.seek(0)
            json.dump(existing_data, f, indent=4)
        return jsonify({"message": "Data saved successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True)