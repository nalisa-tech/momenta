# events/urls.py
from django.urls import path, include
from django.conf import settings
from . import views

app_name = "events"

urlpatterns = [
    path("", views.home, name="home"),
    path("health/", views.health_check, name="health_check"),  # Health check for Railway
    path("event/<int:event_id>/", views.event_detail, name="event_detail"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path("book/<int:event_id>/", views.book_event, name="book_event"),
    path("categories/", views.categories_with_events, name="categories_with_events"),
    path("events/", views.events_list, name="events_list"),
    
    # Payment flow
    path("select-seat/<int:event_id>/", views.select_seat, name="select_seat"),
    path("payment/<int:event_id>/", views.payment_page, name="payment_page"),
    
    # Admin payment actions (accessible from admin interface)
    path("admin/approve-payment/<int:payment_id>/", views.approve_payment, name="approve_payment"),
    path("admin/reject-payment/<int:payment_id>/", views.reject_payment, name="reject_payment"),
    
    # User profile
    path("profile/", views.user_profile, name="profile"),
    
    # Newsletter subscription
    path("subscribe/", views.subscribe_newsletter, name="subscribe"),
    
    # Venue and Resource Management
    path("venues/", views.venues_list, name="venues_list"),
    path("venue/<int:venue_id>/", views.venue_detail, name="venue_detail"),
    path("resources/", views.resources_list, name="resources_list"),
    path("facilities/", views.facilities_public, name="facilities_public"),
    path("admin/facilities/", views.facilities_dashboard, name="facilities_dashboard"),
    
    # NEW: One dynamic URL for ALL categories (must be last as it's a catch-all)
    path("<slug:slug>/", views.category_detail, name="category_detail"),
]

# Developer tools URLs are handled in main urls.py