from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets,generics, status
from .models import Product,Order
from .serializers import ProductSerializer,OrderSerializer
from django.contrib.auth.models import User



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@api_view(['GET'])
def index(req):
    return Response('hello')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
 
        # Add custom claims
        token['username'] = user.username
        # ...
 
        return token
 
 
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# test private area
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def about(req):
    return Response("about")


# register
@api_view(['POST'])
def register(request):
    user = User.objects.create_user(
                username=request.data['username'],
                email=request.data['email'],
                password=request.data['password']
            )
    user.is_active = True
    user.is_staff = True
    user.save()
    return Response("new user born")


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can create orders

    def create(self, request, *args, **kwargs):
        cart_items = request.data  # Assuming the cart items are sent in the request body
        orders = []
        
        for item in cart_items:
            product_id = item['id']
            quantity = item['amount']
            
            try:
                product = Product.objects.get(id=product_id)
                order = Order(user=request.user, product=product, quantity=quantity)  # Set the user
                orders.append(order)
            except Product.DoesNotExist:
                return Response({'error': f'Product with id {product_id} does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        # Save all orders in a bulk operation
        Order.objects.bulk_create(orders)
        
        return Response({'message': 'Order placed successfully!'}, status=status.HTTP_201_CREATED)
    
# get my orders 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(req):
    print(req.user)
    user= req.user
    serializer = OrderSerializer(user.order_set.all(), many=True)
    return Response(serializer.data)