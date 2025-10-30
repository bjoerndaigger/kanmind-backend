from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistrationSerializer


class RegistrationView(APIView):
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

    def post(self,request):
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
            data = serializer.errors

        return Response(data, status=status.HTTP_201_CREATED)
