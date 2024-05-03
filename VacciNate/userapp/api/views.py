from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta
from fcm_django.models import FCMDevice

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request): 
    refresh_token = request.data.get("refresh")
    if refresh_token is None:
        return Response({'error': 'No refresh token provided'}, status=status.HTTP_400_BAD_REQUEST)
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
            token = RefreshToken.for_user(account)
            data['token'] = {
                'refresh': str(token),
                'access': str(token.access_token),
            }
            
        else:
            data = serializer.errors
            
        return Response(data=data, status=status.HTTP_201_CREATED)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_device(request):
    if request.method == 'POST':
        if not request.data.get('registration_id') or not request.data.get('type'):
            return Response(data = "Provide registration_id and type", status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('type') not in ['ios', 'android']:
            return Response(data = "Invalid type choose from: ios/android/web", status=status.HTTP_400_BAD_REQUEST)
        if FCMDevice.objects.filter(registration_id=request.data.get('registration_id')).exists():
            return Response(data = "Device already exists if you have changed device run patch request", status=status.HTTP_400_BAD_REQUEST)
        device = FCMDevice()
        device.registration_id = request.data.get('registration_id')
        device.type = request.data.get('type')
        device.user = request.user
        device.user_id = request.user.id
        device.save()
    
        return Response(data = "Device added", status=status.HTTP_201_CREATED)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_device(request):
    if request.method == 'PATCH':
        if not request.data.get('registration_id') or not request.data.get('type'):
            return Response(data = "Provide registration_id and type", status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('type') not in ['ios', 'android']:
            return Response(data = "Invalid type choose from: ios/android/web", status=status.HTTP_400_BAD_REQUEST)
        if not FCMDevice.objects.filter(registration_id=request.data.get('registration_id')).exists():
            return Response(data = "Device does not exist", status=status.HTTP_400_BAD_REQUEST)
        device = FCMDevice.objects.get(registration_id=request.data.get('registration_id'))
        device.type = request.data.get('type')
        device.save()
    
        return Response(data = "Device updated", status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)