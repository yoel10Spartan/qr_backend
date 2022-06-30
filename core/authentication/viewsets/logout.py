from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import logout

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logout_user(request):
    logout(request)
    return Response('User Logged out successfully')