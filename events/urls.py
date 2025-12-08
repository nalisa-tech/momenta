# events/urls.py
from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("", views.home, name="home"),
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
    path("payment/<int:payment_id>/approve/", views.approve_payment, name="approve_payment"),
    path("payment/<int:payment_id>/reject/", views.reject_payment, name="reject_payment"),
    
    # User profile (must come before category_detail to avoid conflict)
    path("profile/", views.user_profile, name="profile"),
    
    # Newsletter subscription
    path("subscribe/", views.subscribe_newsletter, name="subscribe"),
    
    # NEW: One dynamic URL for ALL categories (must be last as it's a catch-all)
    path("<slug:slug>/", views.category_detail, name="category_detail"),
]