from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CustomLoginEmailOnlySerializer, RegistrationSerializer


class RegistrationAPIView(APIView):
    """
    Register a new user and return an authentication token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            saved_account = serializer.save()

            token, created = Token.objects.get_or_create(user=saved_account)

            data = {
                'token': token.key,
                'fullname': saved_account.first_name,
                'email': saved_account.email,
                'user_id': saved_account.pk
            }
        else:
            data = serializer._errors

        return Response(data, status=status.HTTP_201_CREATED)


class CustomLoginView(ObtainAuthToken):
    """
    Authenticate a user using email and password, returning a token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomLoginEmailOnlySerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

            data = {
                'token': token.key,
                'fullname': user.first_name,
                'email': user.email,
                'user_id': user.pk
            }
            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view()
def email_check_view(request):
    """
    Check if a user exists with the provided email.
    Returns user details if found.
    """
    email = request.query_params.get('email')
    
    if not email:
        return Response({"Error": "Email missing"}, status=status.HTTP_400_BAD_REQUEST)
    if '@' not in email or '.' not in email:
        return Response({"Error": "Invalid email format"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
        return Response({
            "id": user.id,
            "email": user.email,
            "fullname": user.first_name
        })
    except User.DoesNotExist:
        return Response({"Error": "Email not found"}, status=status.HTTP_404_NOT_FOUND)
