from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.core import serializers
import json
from .models import Post
from .serializers import PostSerializer

# APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

# Create your views here.

# CRUD 메서드 (FBV)
  
@require_http_methods(["GET"])    
def get_all_title(request):
    posts = Post.objects.all()
    title_list = []
    
    for post in posts:
        title = post.title
        title_list.append(title)
    
    return JsonResponse({
        "status" : 200,
        "message" : "타이틀 조회 성공",
        "result" : title_list
    })    
    
# CBV

class PostList(APIView):
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'status' : 200,
                'message' : '생성 성공',
                'result' : serializer.data
            })
        else:
            return JsonResponse({
                'status' : 400,
                'message' : '유효하지 않은 데이터',
                'result' : None
            })

class PostDetail(APIView):
    def get(self, request, title):
        post = get_object_or_404(Post, title = title)
        serializers = PostSerializer(post)
        return JsonResponse({
            'status' : 200,
            'message' : '조회 성공',
            'result' : serializers.data
        })
    
    def patch(self, request, title):
        post = get_object_or_404(Post, title = title)
        request.data["title"] = title
        serializers = PostSerializer(post, data=request.data) 
        if serializers.is_valid():
            serializers.save()
            return JsonResponse({
            'status' : 200,
            'message' : '수정 성공',
            'result' : serializers.data
        })
        else:
            return JsonResponse({
                'status' : 400,
                'message' : '유효하지 않은 데이터',
                'result' : None
            })
    
    def delete(self, request, title):
        post = get_object_or_404(Post, title = title)
        post.delete()
        return JsonResponse({
            'status' : 200,
            'message' : '삭제 성공',
            'result' : None
        })
# 오류 처리
    
def handler404(request, exception):
    return JsonResponse({
        'status' : 404,
        'message' : '404 Not Found Error',
        'result' : None
    })