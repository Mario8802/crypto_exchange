from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect  # Import redirect for root URL redirection

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # Include the accounts app URLs

    # Redirect root URL to the login page or home page
    path('', lambda request: redirect('login')),  # Redirect to the login page
]
 
