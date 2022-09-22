from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from .models import Product, CartProduct, Order
from .serializers import OrderSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.



@api_view(['GET'])
def apiOverview(request):
    api_urls = [
        {"User Order History": "my-orders/", "method":"POST", "require": "Authentication Token"},
        {"User Registration": "register-api/", "method":"POST", "require": "username, email, password"},
        {"User update": "update-api/", "method":"POST", "require": "Authentication Token"},
        {"User login with API": "login-api/>", "method":"POST", "require": "Authentication Token and User Credentials"},
        {"User login with webpage": "login/>", "method":"POST", "require": "Authentication Token"},
        {"Products List and Cart to add products to Order": "all-products/", "method":"GET"}
    ]

    return Response(api_urls)


def productsList(request):
    products = Product.objects.all()
    cart = ''
    orders = ''
    user_cart = []
    if request.user.is_authenticated:
        cart = request.user.cart_products.all()
        orders = request.user.ordered_products.all()
        user_cart = cart.values_list('product_id', flat=True)
        print(list(user_cart))
    context = {
        'products': products,
        'cart': cart,
        'orders': orders,
        'user_cart': list(user_cart)
    }
    return render(request, 'product/product-list.html', context)





def addToCart(request, pk):
    product = Product.objects.get(id=pk)
    cart_product, created = CartProduct.objects.get_or_create(product=product, user=request.user)

    return redirect('products-list')



def Increment(request, pk):
    cart_product = CartProduct.objects.get(id=pk, user=request.user)
    cart_product.quantity += 1 
    cart_product.save()

    return redirect('products-list')




def rmvFromCart(request, pk):
    # product = Product.objects.get(id=pk)
    cart_product = CartProduct.objects.get(id=pk, user=request.user)

    if cart_product.quantity > 1:
        cart_product.quantity -= 1
        cart_product.save()
    elif cart_product.quantity == 1:
        cart_product.delete()

    return redirect('products-list')



def placeOrder(request):
    if request.method == 'POST':
        order_list = []
        cart_products = request.user.cart_products.all()
        if cart_products.count() >= 1:
            for cart_product in cart_products:
                order = Order(
                    product=cart_product.product, 
                    user=cart_product.user, 
                    quantity=cart_product.quantity, full_price=cart_product.full_price, title=cart_product.product.title, description=cart_product.product.description, price=cart_product.product.price
                    )

                order_list.append(order)

            orders = Order.objects.bulk_create(order_list)
            cart_products.delete()

    return redirect('products-list')




@api_view(['POST'])
def orderList(request):
    user = request.user

    if user.is_authenticated:
        orders = user.ordered_products.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    return Response({'error': 'not authenticated'}, status=400)