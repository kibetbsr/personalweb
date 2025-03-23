import requests
import base64
from requests.auth import HTTPBasicAuth
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import GuestEntry  # Ensure Message is correctly imported
from .forms import GuestEntryForm
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.conf import settings
from datetime import datetime
from threading import Lock
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm





 # Ensure this is correct
import json
import os



def home(request):
    if request.method == 'POST':
        form = GuestEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to clear the form after submission
    else:
        form = GuestEntryForm()

    # Retrieve messages and unread count
    messages = GuestEntry.objects.all().order_by('-created_at')  
    new_messages_count = GuestEntry.objects.filter(is_read=False).count()

    # Pagination setup (9 messages per page)
    paginator = Paginator(messages, 9)  
    page_number = request.GET.get('page')  
    messages = paginator.get_page(page_number)

    # Render the home.html template (which extends bases.html)
    return render(request, 'base/home.html', {
        'form': form,
        'messages': messages,
        'new_messages_count': new_messages_count
    })


def message_detail(request, pk):
    message = get_object_or_404(GuestEntry, id=pk)
    if not message.is_read:
        message.is_read=True
        message.save()
    return render(request, 'base/message_detail.html', {'message': message})




class NewsAPIClient:
    _instance = None  

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NewsAPIClient, cls).__new__(cls)
            cls._instance.api_providers = {
                "newsapi": {
                    "api_key": "d963bd9548614542bf01cee912a46e47",
                    "base_url": "https://newsapi.org/v2/top-headlines?country=us"
                },
                "mediastack": {
                    "api_key": "YOUR_MEDIASTACK_API_KEY",
                    "base_url": "http://api.mediastack.com/v1/news?countries=us"
                },
                "newscatcher": {
                    "api_key": "YOUR_NEWSCATCHER_API_KEY",
                    "base_url": "https://api.newscatcherapi.com/v2/latest_headlines?countries=US"
                }
            }
            cls._instance.selected_provider = "newsapi"  # Default provider
        
        return cls._instance

    def set_provider(self, provider_name):
        """Dynamically switch between different news API providers."""
        if provider_name in self.api_providers:
            self.selected_provider = provider_name
        else:
            raise ValueError(f"Unknown news provider: {provider_name}")

    def get_news(self):
        """Fetch news from the selected API provider."""
        provider = self.api_providers[self.selected_provider]
        url = f"{provider['base_url']}&apiKey={provider['api_key']}"

        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            articles.sort(key=lambda x: x.get("publishedAt", ""), reverse=True)
            return articles
    
        return []  # hii inareturn an empty list if the API request fails

#add serach algorithm here 
    def search_news(self, articles, query):
        """Search news titles and ensure results are sorted by date."""
        query = query.lower()
        filtered_articles = [article for article in articles if query in article["title"].lower()]
        #  Ensure search results are also sorted by date
        filtered_articles.sort(key=lambda x: x.get("publishedAt", ""), reverse=True)
        return filtered_articles



def get_news(request, provider="newsapi"):
    """Fetch and search news, ensuring results are sorted by most recent."""
    news_api = NewsAPIClient()
    news_api.set_provider(provider)  
    articles = news_api.get_news()  

    search_query = request.GET.get("search", "").strip()  
    if search_query:
        articles = news_api.search_news(articles, search_query)

    return render(request, 'base/news.html', {'articles': articles, 'search_query': search_query})


@login_required
def laws_view(request):
    return render(request, "base/laws.html")  # ✅ Ensure "base/laws.html" is the correct path# Ensure you have a template named laws.html



def forex_rates(request):
    # Fetch Forex Rates
    api_key = "39a2c7571686b29116702da54fd618b7"
    forex_url = f"http://api.currencylayer.com/live?access_key={api_key}&currencies=EUR,GBP,KES,INR,JPY&source=USD"

    forex_response = requests.get(forex_url)
    forex_data = forex_response.json()

    rates = forex_data.get('quotes', {"error": "Failed to retrieve exchange rates"})

    # Fetch Country List
        # Pass both datasets to the template
    return render(request, 'forex.html', {'rates': json.dumps(rates), })


#We now need a view to handle API requests (GET, POST, etc.).

#class CountryViewSet(viewsets.ModelViewSet):
 #   queryset=Country.objects.all() #this gets the records for all cpountries
  #  serializer_class = CountrySerializers


def stkpayment(request):
    return render(request, 'base/about.html')



 #MPESA INTEGRATION


# Singleton MpesaFactory class
class MpesaFactory:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MpesaFactory, cls).__new__(cls)
            cls._instance.init_mpesa()
        return cls._instance

    def init_mpesa(self):
        """Initialize M-Pesa credentials"""
        self.business_shortcode = getattr(settings, "MPESA_SHORTCODE", None)  # Your Till Number
        self.consumer_key = getattr(settings, "MPESA_CONSUMER_KEY", None)
        self.consumer_secret = getattr(settings, "MPESA_CONSUMER_SECRET", None)

        if not all([self.business_shortcode, self.consumer_key, self.consumer_secret]):
            raise ValueError("M-Pesa credentials are missing from settings.py")

        self.access_token = self.get_access_token()

    def get_access_token(self):
        """Generates OAuth token for authentication"""
        api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        response = requests.get(api_url, auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret))

        try:
            return response.json().get("access_token")
        except ValueError:
            raise Exception("Error: Invalid JSON response from Safaricom API when fetching access token.")

    def generate_password(self):
        """Generate the encrypted password for STK Push"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # For Till Number transactions, no passkey is required
        password = f"{self.business_shortcode}{timestamp}"
        encoded_password = base64.b64encode(password.encode()).decode()
        
        return encoded_password, timestamp

    def stk_push(self, amount, phone_number):
        """Initiate STK Push request for a Till Number"""
        password, timestamp = self.generate_password()
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "BusinessShortCode": self.business_shortcode,  # Your Till Number
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerBuyGoodsOnline",  # Correct for Till Number payments
            "Amount": int(amount),
            "PartyA": phone_number,
            "PartyB": self.business_shortcode,  # Your Till Number
            "PhoneNumber": phone_number,
            "CallBackURL": "https://yourwebsite.com/callback/",
            "AccountReference": "Order123",
            "TransactionDesc": "Payment for Services"
        }

        try:
            response = requests.post(api_url, json=payload, headers=headers)
            return response.json()
        except ValueError:
            raise Exception("Error: Invalid JSON response from Safaricom API during STK Push.")

# Create a single instance of MpesaFactory (Singleton)
mpesa_instance = MpesaFactory()

# View function to handle STK Push when clicking the M-Pesa logo
def process_payment(request):
    phone_number = "2547XXXXXXXX"  # Replace with actual number
    amount = 100  # Replace with actual amount
    response = mpesa_instance.stk_push(amount, phone_number)
    return JsonResponse(response)



#LOgING AND SIGNUO




def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]

            # Check if username or email already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is already taken. Choose another.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered. Use another.")
            else:
                user = form.save(commit=False)
                user.email = email  # Ensure email is saved
                user.save()
                messages.success(request, "Account created successfully! You can now log in.")
                return redirect("login")  # Redirect to login page

    else:
        form = CustomUserCreationForm()

    return render(request, "base/signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("about")  # Redirect to about page after login
    else:
        form = AuthenticationForm()
    return render(request, "base/login.html", {"form": form})


def logout_view(request):
        #logging out
    logout(request)
    messages.success(request, "Logout Successful")

    return redirect("home")



def about_view(request):
    return render(request, "base/about.html")  # Ensure correct pat