from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from User.api.serializers import VendorRegistrationSerializer
from User import models

@api_view(['POST',])
def logout_view(request):

    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
    
@api_view(['POST',])
def vendor_registration_view(request):

    if request.method == 'POST':
        serializer = VendorRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            account = serializer.save()
            token = Token.objects.get(user=account).key
            return Response({
                'response': "Registration Successful!",
                'name': account.username,
                'token': token
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
