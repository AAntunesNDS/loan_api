"""
URL configuration for loans project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api_loans.api.viewsets import EmprestimoViewSet, PagamentoViewSet
from api_loans.views import MyTokenObtainPairView, MyTokenRefreshView

route = routers.DefaultRouter()
route.register(r"loans", EmprestimoViewSet, basename="Loans")
route.register(r"payment", PagamentoViewSet, basename="Payment")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(route.urls)),
    path("api/token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", MyTokenRefreshView.as_view(), name="token_refresh"),
]
