from django.urls import path
from .views import home_view, RegisterView, CustomTokenObtainPairView, BuyVTUView, buy_airtime
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', home_view),  # homepage for the app
    path('register/', RegisterView.as_view()),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('buy/', BuyVTUView.as_view()),
    path('buy-airtime/', buy_airtime, name='buy_airtime'),
]
