from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Create your views here.
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def CartPage(request):
    data = {
        'order' : None
    }

    user = request.user
    order, created = OrderModel.objects.get_or_create(user = user, ordered = False)
    orderItems = OrderItemModel.objects.filter(order = order)

    if not orderItems.exists():
        data = {'Response' : 'Your Shopping Cart is Empty'}
        return Response(data, status=status.HTTP_200_OK)

    orderItemSerializer = CartOrderItemSerializer(orderItems, many = True)
    data['order'] = orderItemSerializer.data
    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddProduct(request, productId):
    try:
        product = ProductModel.objects.get(id = productId)
    except ProductModel.DoesNotExist:
        data = {'Error' : 'Product Does Not Exists'}
        return Response(data)

    user = request.user
    order, created = OrderModel.objects.get_or_create(user=user, ordered=False) 

    orderItem, created = OrderItemModel.objects.get_or_create(product=product, order=order)
    orderItem.quantity = (orderItem.quantity + 1)
    orderItem.save()

    data = {'Response' : 'Product Added Successfully'}
    return Response(data, status=status.HTTP_201_CREATED)
       
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def RemoveProduct(request, orderItemId):
    try:
        orderItem = OrderItemModel.objects.get(id = orderItemId)
    except OrderItemModel.DoesNotExist:
        data = {'Error' : 'OrderItem Does Not Exists'}
        return Response(data)

    orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    data = {'Response' : 'Product Deleted Succesfully'}
    return Response(data, status=status.HTTP_200_OK)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def ShippingAddressScreen(request):
    data = {
        'ShippingInfo' : None,
        'order' : None,
    }

    user = request.user
    order, created = OrderModel.objects.get_or_create(user = user, ordered = False)
    orderItems = OrderItemModel.objects.filter(order = order)

    try:
        shippingInfo = ShippingAddressModel.objects.get(order = order)
        shippingInfoSerializer = CartShippingAddressSerializer(shippingInfo, many = False)
        data['ShippingInfo'] = shippingInfoSerializer.data
    except ShippingAddressModel.DoesNotExist:
        data['ShippingInfo'] = 'No Shipping Info'

    if not orderItems.exists():
        data = {'Response' : 'Your Shopping Cart is Empty'}
        return Response(data, status=status.HTTP_200_OK)

    orderItemSerializer = CartOrderItemSerializer(orderItems, many = True)
    data['order'] = orderItemSerializer.data
    return Response(data, status=status.HTTP_200_OK)

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def AddShippingAddress(request):
    shippingSerializer = CartShippingAddressSerializer(data = request.data)
    if shippingSerializer.is_valid():
        shippingSerializer.save()
        data = {'Response' : 'Shipping Address Added Succesfully'}
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data = {'Error' : 'Shipping Address Is Not Valid'}
        return Response(data, status=status.HTTP_200_OK)
    
@permission_classes([IsAuthenticated])
@api_view(['PUT'])
def EditShippingAddress(request, orderId):
    try:
        shippingInfo = ShippingAddressModel.objects.get(order = orderId)
    except ShippingAddressModel.DoesNotExist:
        data = {'Response' : 'This shipping info does not exists'}
        return Response(data, status=status.HTTP_200_OK)

    shippingSerializer = CartShippingAddressSerializer(data = request.data, instance = shippingInfo)
    
    if shippingSerializer.is_valid():
        shippingSerializer.save()
        data = {'Response' : 'Shipping Address Added Succesfully'}
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data = {'Error' : 'Shipping Address Is Not Valid'}
        return Response(data, status=status.HTTP_200_OK)
    
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def PaymentPage(request):
    data = {
        'ShippingInfo' : None,
        'order' : None
    }

    user = request.user
    order, created = OrderModel.objects.get_or_create(user = user, ordered = False)
    orderItems = OrderItemModel.objects.filter(order = order)

    try:
        shippingInfo = ShippingAddressModel.objects.get(order = order)
        shippingInfoSerializer = CartShippingAddressSerializer(shippingInfo, many = False)
        data['ShippingInfo'] = shippingInfoSerializer.data
    except ShippingAddressModel.DoesNotExist:
        data['ShippingInfo'] = 'No Shipping Info'

    if not orderItems.exists():
        data = {'Response' : 'Your Shopping Cart is Empty'}
        return Response(data, status=status.HTTP_200_OK)

    orderItemSerializer = CartOrderItemSerializer(orderItems, many = True)
    data['order'] = orderItemSerializer.data
    return Response(data, status=status.HTTP_200_OK)