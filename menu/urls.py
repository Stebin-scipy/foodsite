from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('food/<int:id>/', views.food_detail, name='food_detail'),
    path('category/<int:category_id>/', views.category_view, name='category_view'),
    path('special-offers/', views.special_offers, name='special_offers'),
    path('cart/', views.cart, name='cart'),
    path('signup/', views.signup, name='signup'),
    path('add-to-cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('rate/<int:food_id>/', views.rate_food, name='rate_food'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),



]
    