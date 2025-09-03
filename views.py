from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, TransactionSerializer
from .models import Transaction
import requests
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import render
import uuid
from .utils import vtpass_auth_headers
from django.http import JsonResponse
from django.shortcuts import render
from django.http import JsonResponse
from .utils import vtpass_post
from django.shortcuts import render

def buy_airtime(request):
    context = {}  # or add any context variables you want here
    return render(request, 'buy_airtime.html', context)


def home_view(request):
    return render(request, 'index.html')


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

class BuyVTUView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    def perform_create(self, serializer):
        tx = serializer.save(user=self.request.user)
        tx_id = str(uuid.uuid4())

        data = {
            "request_id": tx_id,
            "serviceID": tx.network,  # e.g., "mtn"
            "amount": tx.amount,
            "phone": tx.phone
        }

        headers = vtpass_auth_headers('YOUR_VTPASS_EMAIL', 'YOUR_VTPASS_PASSWORD')
        response = requests.post(
            'https://vtpass.com/api/pay',
            headers=headers,
            json=data
        )
        
        tx.provider_response = response.text
        tx.success = response.status_code == 200
        tx.save()
        # vtu/views.py


def airtime_recharge(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        amount = request.POST.get("amount")
        network = request.POST.get("network")  # e.g. mtn, glo
        request_id = str(uuid.uuid4())

        vtpass = VTPassAPI()
        result = vtpass.purchase_airtime(phone, amount, network, request_id)
        return JsonResponse(result)
    return render(request, "airtime_form.html") 

def buy_airtime_api(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        amount = request.POST.get("amount")
        network = request.POST.get("network")  # e.g. "mtn", "airtel"

        payload = {
            "request_id": "unique_id_12345",  # generate uniquely
            "serviceID": network,
            "amount": amount,
            "phone": phone
        }

        result = vtpass_post("pay", payload)
        return JsonResponse(result)
    return JsonResponse({"error": "Invalid request method"}, status=400)
    