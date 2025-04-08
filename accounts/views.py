import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import CategorySerializer, SignupSerializer, LoginSerializer  # make sure this exists


@api_view(['GET', 'POST'])
def category_list_create(request):
    """
    List all categories or create a new category.
    """
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['POST'])
def signup_view(request):
    """User signup view with validation."""
    serializer = SignupSerializer(data=request.data)  #
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_view(request):
    """User login view that returns JWT tokens."""
    serializer = LoginSerializer(data=request.data)  # ✅ Use request.data
    if serializer.is_valid():
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response({
            'data': {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'id': user.id,
                'email': user.email,
                'username': user.username,
            }
        })
    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)