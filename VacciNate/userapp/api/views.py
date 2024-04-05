from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request): 
    refresh_token = request.data["refresh"]
    token = RefreshToken(refresh_token)
    token.blacklist()
    return Response(status=status.HTTP_205_RESET_CONTENT)


@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'successfully registered new user.'
            data['email'] = account.email
            data['username'] = account.username
            
            # ---JWT Token---
        
            token = RefreshToken.for_user(account)
            data['token'] = {
                'refresh': str(token),
                'access': str(token.access_token),
            }
            
        else:
            data = serializer.errors
            
        return Response(data=data, status=status.HTTP_201_CREATED)