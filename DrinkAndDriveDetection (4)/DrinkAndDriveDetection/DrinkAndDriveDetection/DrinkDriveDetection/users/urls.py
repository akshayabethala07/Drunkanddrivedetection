from django.urls import path
from . import views

urlpatterns = [
    # Basic views
    path('', views.index, name='index'),  # Home page
    path('login/', views.login_view, name='login'),  # Login page
    path('accounts/login/', views.login_view, name='account_login'),  # Alias for account login (standard path for Django auth)
    path('register/', views.Register1, name='register'),  # Registration page
    path('profile/', views.profile_view, name='profile'),  # Profile page (only accessible when logged in)
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),  # Edit profile page (only accessible when logged in)
    path('logout/', views.logout_view, name='logout'),  # Logout and session clear
    
    # Predict functionality
    path('predict_drink_driving/', views.Predict_Drink_Driving_Detection, name='predict_drink_driving'),  # Page for drink driving prediction functionality

    # API-like endpoints for dynamic dropdowns (returns JSON for gender, state, city data)
    path('get_states/<int:country_id>/', views.get_states, name='get_states'),  # Get states based on selected country
    path('get_cities/<int:state_id>/', views.get_cities, name='get_cities'),  # Get cities based on selected state
    path('get_genders/', views.get_genders, name='get_genders'),  # Get all gender options
]
