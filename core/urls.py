from django.urls import path
from . import views
from .views import create_admin

urlpatterns = [
    path('', views.home, name='home'),
    path('create-admin/', create_admin),
    path('book/<int:provider_id>/', views.book_provider, name='book_provider'),
    path('success/', views.booking_success, name='booking_success'),
    path('bookings/', views.view_bookings, name='view_bookings'),
    # ↓ new ones:
    path('signup/', views.signup, name='signup'),
    path('login/',  views.login_view,  name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('review/<int:booking_id>/', views.leave_review, name='leave_review'),
    # Merge these two paths
    path('provider-reviews/<int:provider_id>/', views.provider_reviews, name='provider_reviews'),
    # Cooking service URLs
    path('cooking-services/', views.cooking_services, name='cooking_services'),
    path('veg-dishes/', views.veg_dishes, name='veg_dishes'),
    path('non-veg-dishes/', views.non_veg_dishes, name='non_veg_dishes'),
    path('add-dish/', views.add_dish, name='add_dish'),
    path('order-dish/', views.order_dish, name='order_dish'),
    path('order-dish/<int:dish_id>/', views.order_dish, name='order_dish'),
    path('booking-confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    # Service URLs
    path('services/', views.services, name='services'),
    path('services/<int:service_id>/', views.service_detail, name='service_detail'),
    path('save-food-selection/', views.save_food_selection, name='save_food_selection'),
]
