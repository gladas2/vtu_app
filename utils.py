import base64
import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth
import uuid
from .utils import vtpass_auth_headers 

def vtpass_auth_headers(username, password):
    credentials = f"{username}:{password}"
    token = base64.b64encode(credentials.encode()).decode()
    return {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json"
    }


def vtpass_post(endpoint, payload):
    url = settings.VTPASS_BASE_URL + endpoint
    auth = HTTPBasicAuth(settings.VTPASS_USERNAME, settings.VTPASS_PASSWORD)

    headers = {
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(url, json=payload, headers=headers, auth=auth)
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}


class VTPassAPI:
    BASE_URL = "https://vtpass.com/api/"

    def __init__(self, email=None, password=None):
        # Use env variables or pass credentials here
        self.email = email or "YOUR_VTPASS_EMAIL"
        self.password = password or "YOUR_VTPASS_PASSWORD"
        self.headers = vtpass_auth_headers(self.email, self.password)

    def purchase_airtime(self, phone, amount, network, request_id=None):
        if request_id is None:
            request_id = str(uuid.uuid4())

        payload = {
            "request_id": request_id,
            "serviceID": network,
            "amount": amount,
            "phone": phone
        }

        url = self.BASE_URL + "pay"
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()  # Raises HTTPError for bad responses
            return response.json()
        except requests.RequestException as e:
            # Log or handle error properly
            return {"error": str(e)}
