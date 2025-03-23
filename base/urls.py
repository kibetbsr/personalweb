from django.urls import path, include
from . import views
from .views import home, get_news 
from .views import process_payment  # Import the view
from .views import laws_view 
from .views import signup_view, login_view, logout_view, about_view



#from rest_framework.routers import DefaultRouter 
# Create a router to generate API endpoints automatically
#router = DefaultRouter()
#router.register(r'countries', CountryViewSet) #this creates endpiunts kama hizi: GET /api/countries/ → Get all countries
#POST /api/countries/ → Add a new country
#GET /api/countries/{id}/ → Get details of a specific country
#PUT/PATCH /api/countries/{id}/ → Update a country
#DELETE /api/countries/{id}/ → Delete a country

urlpatterns = [
    path('', home, name='home'),  # Home page with the form
    path('message/<str:pk>/', views.message_detail, name='message_detail'),
    path('news/', views.get_news, name = 'news'),
    path('forex/', views.forex_rates, name = 'forex'), 
    path('about/', views.about_view, name='about'),
    path("stk-push/", process_payment, name="stk_push"),  # Route for STK Push
    path('laws/', views.laws_view, name="laws"),  # Define the 'laws' URL pattern
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

  #  path('api', include(router.urls)), 
    
   
]


