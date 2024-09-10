from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile, Transaction

# User login view
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(f"Attempting login for: {username}")  # Debugging line
        user = authenticate(request, username=username, password=password)

        if user is not None:
            print(f"User {user.username} authenticated successfully")  # Debugging line
            login(request, user)
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            print("Authentication failed")  # Debugging line
            messages.error(request, 'Invalid credentials')

    return render(request, 'accounts/login.html')

# User logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# User registration view
def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                messages.success(request, 'Registration successful')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')

    return render(request, 'accounts/register.html')

# Dashboard view
@login_required
def dashboard_view(request):
    user_profile = UserProfile.objects.get(user=request.user)

    # Simulated cryptocurrency prices
    cryptocurrencies = [
        {'name': 'Bitcoin', 'symbol': 'BTC', 'price': 57605.07},
        {'name': 'Ethereum', 'symbol': 'ETH', 'price': 2374.27},
        {'name': 'Solana', 'symbol': 'SOL', 'price': 135.43},
    ]

    context = {
        'balance': user_profile.balance,
        'cryptocurrencies': cryptocurrencies,
    }

    return render(request, 'accounts/dashboard.html', context)

# Buy Crypto view
@login_required
def buy_crypto_view(request):
    if request.method == 'POST':
        crypto = request.POST['crypto']
        amount = float(request.POST['amount'])
        user_profile = UserProfile.objects.get(user=request.user)

        # Simulated crypto prices
        crypto_prices = {'BTC': 57605.07, 'ETH': 2374.27, 'SOL': 135.43}
        if crypto in crypto_prices:
            price = crypto_prices[crypto]
            total_cost = amount * price

            if user_profile.balance >= total_cost:
                user_profile.balance -= total_cost
                user_profile.save()

                Transaction.objects.create(
                    user=request.user,
                    crypto_name=crypto,
                    amount=amount,
                    transaction_type='buy'
                )

                messages.success(request, f'Successfully purchased {amount} {crypto} for ${total_cost:.2f}')
            else:
                messages.error(request, 'Insufficient balance')

        return redirect('dashboard')

    return render(request, 'accounts/buy_crypto.html')
