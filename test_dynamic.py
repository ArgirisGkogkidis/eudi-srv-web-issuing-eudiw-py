#!/usr/bin/env python3
import requests
import json
import base64

def test_dynamic_endpoint():
    # Base URL
    base_url = "https://eudi-issuer.codeinu.gr"
    
    # 1. Get token (if needed)
    token_url = f"{base_url}/token"
    token_data = {
        "grant_type": "client_credentials",
        "client_id": "your_client_id",
        "client_secret": "your_client_secret"
    }
    
    token_response = requests.post(token_url, data=token_data)
    token = token_response.json().get("access_token")
    
    # 2. Create authorization details
    auth_details = [
        {
            "credential_configuration_id": "pid_jwt_vc",
            "format": "jwt_vc_json"
        }
    ]
    
    # 3. Create session data
    session_data = {
        "authorization_params": {
            "token": token,
            "authorization_details": json.dumps(auth_details)
        },
        "session_id": "test_session_123"
    }
    
    # 4. Test dynamic endpoint
    dynamic_url = f"{base_url}/dynamic"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # First request - get supported countries
    response = requests.get(dynamic_url, headers=headers)
    print("Supported Countries Response:", response.text)
    
    # 5. Select a country (e.g., GR)
    country_data = {
        "country": "GR",
        "proceed": "true"
    }
    
    # Post country selection
    response = requests.post(dynamic_url, data=country_data, headers=headers)
    print("Country Selection Response:", response.text)
    
    # 6. Test form submission
    form_data = {
        "given_name": "Test",
        "family_name": "User",
        "birth_date": "1990-01-01",
        "age_over_18": "true"
    }
    
    form_url = f"{base_url}/dynamic/form"
    response = requests.post(form_url, data=form_data, headers=headers)
    print("Form Submission Response:", response.text)

if __name__ == "__main__":
    test_dynamic_endpoint() 