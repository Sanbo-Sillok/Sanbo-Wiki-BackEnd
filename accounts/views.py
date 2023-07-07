from django.shortcuts import render

from .serializers import ResisterSerializer, AuthSerializer

#APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

# JWT
from rest_framework_simplejwt.serializers import RefreshToken
    
# 인가
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.
class RegisterView(APIView):
    serializer_class = ResisterSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=False):
            member = serializer.save(request)
            token = RefreshToken.for_user(member)
            refresh_token = str(token)
            access_token = str(token.access_token)
            
            res = Response(
                {
                    "member" : serializer.data,
                    "message" : "register success",
                    "token" : {
                        "access_token" : access_token,
                        "refresh_token" : refresh_token,
                    },
                },
                status= status.HTTP_201_CREATED,
            )
            return res
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AuthView(APIView):
    serializer_class = AuthSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=False):
            member = serializer.validated_data["member"]
            access_token = serializer.validated_data["access_token"]
            refresh_token = serializer.validated_data["refresh_token"]
            
            res = Response(
                {
                    "member" : {
                        "id" : member.id,
                        "email" : member.email,
                        "name" : member.name,
                    },
                    "message" : "login success",
                    "token" : {
                        "access_token" : access_token,
                        "refresh_token" : refresh_token,
                    },
                },
                status = status.HTTP_200_OK
            )
            res.set_cookie("access-token", access_token, secure=True)
            res.set_cookie("refresh-token", refresh_token, secure=True, httponly=True)
            return res
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        res = Response({
            "message" : "logout success"
        }, status=status.HTTP_202_ACCEPTED)
        
        res.delete_cookie("access-token")
        res.delete_cookie("refresh-token")
        return res