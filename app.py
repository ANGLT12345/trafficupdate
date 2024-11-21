from flask import Flask, render_template
import requests

app = Flask(__name__)

# Traffic incidents URL and API key
traffic_url = 'http://datamall2.mytransport.sg/ltaodataservice/TrafficIncidents'
api_key = 'VROVFNeMSI+qIQo/OLuNw=='  # Replace with your actual API key

def fetch_traffic_incidents():
    headers = {
        'AccountKey': 'VROVFNeMSI+qIQ4o/OLuNw==',
        'Accept': 'application/json'
    }

    try:
        print("Sending request to API...")  # Debug: Indicate request is being sent
        response = requests.get(traffic_url, headers=headers)
        print("Response Status Code:", response.status_code)  # Print status code
        print("Response Headers:", response.headers)  # Print response headers

        raw_data = response.text  # Get raw text response
        print("Raw Response:", raw_data)  # Debug: Print raw response content

        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()  # Attempt to parse JSON

        print("API Response:", data)  # Debug: Print the entire API response

        if not data or 'value' not in data:
            print("No valid data found in response.")
            return []

        return data['value']

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Print HTTP errors
        return []
    except Exception as e:
        print(f"Error fetching traffic data: {e}")  # Print other errors
        return []

@app.route('/')
def index():
    incidents = fetch_traffic_incidents()
    print("Fetched Incidents:", incidents)  # Debug: Print fetched incidents

    categorized_incidents = {
        "Roadworks": [],
        "Accidents": [],
        "Breakdowns": [],
        "Other": []
    }

    for incident in incidents:
        incident_type = incident.get('Type', 'Other').lower()
        if 'roadwork' in incident_type:
            categorized_incidents["Roadworks"].append(incident)
        elif 'accident' in incident_type:
            categorized_incidents["Accidents"].append(incident)
        elif 'vehicle breakdown' in incident_type:
            categorized_incidents["Breakdowns"].append(incident)
        else:
            categorized_incidents["Other"].append(incident)

    # Limit roadworks to 3
    categorized_incidents["Roadworks"] = categorized_incidents["Roadworks"][:3]

    return render_template('index.html', incidents=categorized_incidents)

@app.errorhandler(403)
def forbidden(e):
    print(f"Forbidden error: {e}")  # Log the error for debugging
    return render_template('403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    print(f"Page not found error: {e}")  # Log the error for debugging
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    print(f"Internal server error: {e}")  # Log the error for debugging
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug=True)
