from django.shortcuts import render
from django.core.cache import cache
from django.http import JsonResponse

from .serializers import ResisterSerializer, AuthSerializer
from .models import *

#APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

# JWT
from rest_framework_simplejwt.serializers import RefreshToken

# 작성자 정보를 가져오기 위한 복호화 모듈
from rest_framework_simplejwt.tokens import AccessToken
from jwt import exceptions

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
    MAX_LOGIN_ATTEMPTS = 5 
    
    def get_client_ip(self, request):
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            return ip
    
        
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        # 사용자의 IP 주소를 추적 (옵션)
        user_ip = self.get_client_ip(request)
        
        # 로그인 시도 횟수 가져오기
        login_attempts = cache.get(user_ip, 0)


        if login_attempts >= self.MAX_LOGIN_ATTEMPTS:
            # 로그인 시도 횟수가 제한을 초과한 경우
            return JsonResponse(
                {"message": "로그인 시도 횟수 초과. 잠시 후 다시 시도하세요."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        if serializer.is_valid(raise_exception=False):        
            cache.delete(user_ip)               
            member = serializer.validated_data["member"]
            access_token = serializer.validated_data["access_token"]
            refresh_token = serializer.validated_data["refresh_token"]
            
            res = Response(
                {
                    "member" : {
                        "id" : member.id,
                    },
                    "message" : "login success",
                    "token" : {
                        "access_token" : access_token,
                        "refresh_token" : refresh_token,
                    },
                },
                status = status.HTTP_200_OK
            )
            return res
        else:
            login_attempts += 1
            cache.set(user_ip, login_attempts, timeout=1800)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        res = Response({
            "message" : "logout success"
        }, status=status.HTTP_202_ACCEPTED)
        return res