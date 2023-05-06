from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .api.serializers import MyTokenObtainPairSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class MyTokenRefreshView(TokenRefreshView):
    pass
