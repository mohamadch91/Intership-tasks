from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import User
from .serializers import UserSerializer, ProfileSerializer

# Gets all users
@api_view(["GET"])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    return Response(serializer.data)

# Creates a new user
@api_view(["POST"])
def register(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        # Create user in database
        user = serializer.save()
        return Response(
            {
                "message": "Registered succesfully",
                "user": UserSerializer(user).data
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

# Ask users for login details
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    # Get phone and password from user
    phone = request.data.get("phone")
    password = request.data.get("password")
    if not phone or not password:
        return Response(
            {"error": "Phone number and password are both required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(
        request,
        phone=phone,
        password=password
    )

    if user is None:
        return Response(
            {"error": "Invalid phone number or password"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Generate a refresh token for the authenticated user
    refresh = RefreshToken.for_user(user)

    # Return the tokens and user info
    return Response(
        {
        "message": "Login successful",
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user": UserSerializer(user).data,
        },
        status=status.HTTP_200_OK
    )

# Gets users profile and updates profile details
@api_view(["GET", "PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def profile(request):
    # Get current user profile
    if request.method == "GET":
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

    # Updates the current user profile
    serializer = ProfileSerializer(request.user, data=request.data, partial=request.method == "PATCH")

    if serializer.is_valid():
        # Update user in database
        user = serializer.save()
        return Response(
            {"message": "Updated profile",},
            status=status.HTTP_200_OK
        )
    
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
     )

# Deletes profile photo
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_profile_photo(request):
    photo = request.user.photo

    if not photo:
        return Response(
            {"message": "No current photo"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete user profile picture
    request.user.photo.delete()
    return Response(
        {"message": "Profile photo deleteed"},
        status=status.HTTP_200_OK
    )
