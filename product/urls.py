from django.urls import path
from .views import apiOverview, productsList, addToCart, rmvFromCart, Increment, placeOrder, orderList


urlpatterns = [
    path('', apiOverview, name='api-overview'),
    path('all-products/', productsList, name='products-list'),
    path('increment/<str:pk>/', Increment, name='increment'),
    path('add-to-cart/<str:pk>/', addToCart, name='add-to-cart'),
    path('rmv-from-cart/<str:pk>/', rmvFromCart, name='rmv-from-cart'),
    path('order/', placeOrder, name='order'),
    path('my-orders/', orderList, name='my-orders'),
]