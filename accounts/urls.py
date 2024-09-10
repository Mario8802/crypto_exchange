from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),  # Register view
    path('login/', views.login_view, name='login'),      # Login view
    path('logout/', views.logout_view, name='logout'),   # Logout view
    path('dashboard/', views.dashboard_view, name='dashboard'),  # Dashboard view
    path('buy/', views.buy_crypto_view, name='buy_crypto'),  # Buy crypto view
]
