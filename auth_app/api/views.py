from rest_framework.views import APIView
from rest_framework.response import Response

class RegistrationView(APIView):
    def get(self, request):
        return Response({"message": "Endpoint works"})