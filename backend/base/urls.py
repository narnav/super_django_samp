
from django.contrib import admin
from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
urlpatterns = [
    path('', views.index),
    path('get_orders', views.get_orders),
    
    path('register', views.register),
    path('login', views.MyTokenObtainPairView.as_view()),
    path('', include(router.urls)),
    path('orders/', views.OrderCreateView.as_view()),
]
