import datetime

from cryptography.fernet import Fernet
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.conf import settings
from django.urls import reverse
    

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from server.apps.authentication.serializer import NewUserSerializer, UserSerializer
from server.apps.authentication import api


# ----------------- CONSTANTS ----------------- #


SEPARATOR = "***"
KEY = b'BZjdwPZWZnf5DYCVKT9CvqeDNYUA6cV85CTd0dmewzM='


# ----------------- CODE ----------------- #


class AuthenticationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),
            'auth': str(request.auth)
        }
        return Response(content)


@api_view(['POST'])
def sign_up(request, format=None):
    serializer = NewUserSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_user(
            serializer.data['username'],
            email=serializer.data['email'],
            password=serializer.data['password']
        )
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def who_am_i(request, format=None):
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def logout(request, format=None):
    message = {"message": "You successfully have been logged out"}
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response(message, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response (status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT'])
def reset_password(request, format=None):
    if request.method == 'PUT':
        try:
            user = User.objects.get(username=request.data['username'])
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        old_password = request.data.get('password', None)
        new_password = request.data.get('new_password', None)
        if check_password(old_password, user.password): 
            user.set_password(new_password)
            user.save()
            return Response({"new_password" : user.password}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['POST'])
def forgotten_password_initialize(request, format=None):
    try:
        user = User.objects.get(
            username=request.data['username'],
            email=request.data['email'])
        print(user)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    message = f'{datetime.datetime.now().isoformat()}{SEPARATOR}{user.email}'
    format = Fernet(KEY)
    reset_token = format.encrypt(message.encode())
    print(f'this is a format {reset_token} from init')
    new_url = reverse(api.URL_NAME__FORGOTTEN_PASSWORD_FIN, args=[reset_token.decode()])
    return Response({"new_url": new_url}, status=status.HTTP_201_CREATED)
 
    
@api_view(['POST'])
def forgotten_password_finilize(request, token, format=None):
    format = Fernet(KEY)
    decrypt_token = format.decrypt(token).decode()
    time_reset = decrypt_token.split(SEPARATOR)[0]
    old_time = datetime.datetime.fromisoformat(time_reset)
    current_time = datetime.datetime.now()
    hour = datetime.timedelta(hours=1)

    if current_time > old_time + hour:
        message = 'The time limit has expired'
        return Response({'message': message},  status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        try:
            user = User.objects.get(
                username=request.data['username'],
                email=request.data['email'])
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        new_password = request.data.get('new_password', None)
        verify_password = request.data.get('verify_new_password', None)
        if new_password == verify_password:
            user.set_password(new_password)
            user.save()
            old_token = Token.objects.get(user=user)
            old_token.delete()
            new_token = Token.objects.create(user=user)
            return Response({"new auth token": new_token.key}, status=status.HTTP_201_CREATED)
