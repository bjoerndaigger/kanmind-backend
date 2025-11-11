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
    API view for user registration.

    This view allows unauthenticated users to register by sending
    a POST request with required user details. Upon successful 
    registration, an authentication token is created and returned
    along with the user details.

    Attributes:
        permission_classes (list): Permissions for the view (AllowAny to allow public access).
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST request for user registration.

        Args:
            request (Request): The HTTP request object containing registration data.

        Returns:
            Response: A REST framework Response containing either:
                - Success: User data and authentication token (status 201)
                - Failure: Validation errors (status 201, same as DRF default for errors)
        """
        serializer = RegistrationSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            saved_account = serializer.save()

            token, created = Token.objects.get_or_create(user=saved_account)

            data = {
                'token': token.key,
                'fullname': saved_account.username,
                'email': saved_account.email,
                'user_id': saved_account.pk
            }
        else:
            data = serializer._errors

        return Response(data, status=status.HTTP_201_CREATED)


class CustomLoginView(ObtainAuthToken):
    """
    Custom login view using email and password for authentication.

    This view allows users to log in using their email instead of
    the default username. Upon successful authentication, it returns
    an authentication token and basic user information.

    Attributes:
        permission_classes (list): AllowAny permits both authenticated
                                   and unauthenticated users to access this view.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST requests for user login via email.

        Steps:
            1. Initialize the serializer with request data.
            2. Validate the serializer.
            3. If valid:
                a. Retrieve the authenticated user.
                b. Get or create an authentication token.
                c. Return user details and token.
            4. If invalid, return validation errors.

        Args:
            request (Request): The HTTP request containing 'email' and 'password'.

        Returns:
            Response: A REST framework Response containing either:
                - Success: token, fullname, email, and user_id (status 200)
                - Failure: validation errors (status 400)
        """
        serializer = CustomLoginEmailOnlySerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

            data = {
                'token': token.key,
                'fullname': user.username,
                'email': user.email,
                'user_id': user.pk
            }
            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view()
def email_check_view(request):
    """
    API endpoint to check the existence and validity of an email address.

    Query Parameters:
    - email (str): The email address to be checked.

    Responses:
    - 200 OK: Returns user details if the email exists.
        {
            "id": int,
            "email": str,
            "fullname": str
        }
    - 400 Bad Request: Returned if the email parameter is missing or has an invalid format.
        {"Error": "Email missing"} or {"Error": "Invalid email format"}
    - 404 Not Found: Returned if no user exists with the provided email.
        {"Error": "Email not found"}
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
