import json
from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Order, OrderItem
from .models import Product

def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            },
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })

@api_view(['POST'])
def register_order(request):
    order = request.data
    products = order.get('products')
    if isinstance(products, list) and len(products):
        order_obj = Order.objects.create(
            datetime=order.get('datetime'),
            firstname=order.get('firstname'),
            lastname=order.get('lastname'),
            phonenumber=order.get('phonenumber'),
            address=order.get('address')
        )
        for product in products:
            OrderItem.objects.create(
                order=order_obj,
                product=Product.objects.get(id=product.get('product')),
                quantity=product.get('quantity'),
            )
        return Response()
    else: 
        return Response('error! products key not presented or not a list or list is empty',
                         status=status.HTTP_400_BAD_REQUEST,
                       )
