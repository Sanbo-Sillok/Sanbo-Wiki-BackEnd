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

# CRUD 메서드

@require_http_methods(["POST"])    
def create_post(request):
    body = json.loads(request.body.decode('utf-8'))
    
    new_post = Post.objects.create(
           title = body['title'],
           contents = body['contents'], 
       )
    
    new_post_json = {
           "id" : new_post.id,
           "title" : new_post.title,
           "contents" : new_post.contents,
           "created_at" : new_post.created_at
       }
    
    return JsonResponse({
        'status' : 200,
        'message' : '게시글 생성 성공',
        'result' : new_post_json
    })
    
@require_http_methods(["GET", "DELETE", "PATCH"])
def get_or_delete_or_edit_post(request, title):
    post = get_object_or_404(Post, title = title)       

    if request.method == "GET":
    
        post_json = {
            "id" : post.pk,
            "title" : post.title,
            "contents" : post.contents,
            "created_at" : post.created_at      
        }

        return JsonResponse({
                'status' : 200,
                'message' : '게시글 조회 성공',
                'result' : post_json
            })
    elif request.method == "DELETE":
        
        post.delete()
    
        return JsonResponse({
            'status' : 200,
            'message' : '게시글 삭제 성공',
            'result' : None
        })
    elif request.method == "PATCH":
        body = json.loads(request.body.decode('utf-8'))
        update_post = get_object_or_404(Post, title = title)
    
        update_post.contents = body['contents']
            
        update_post.save()
        
        update_post_json = {
            "id" : update_post.id,
            "title" : update_post.title,
            "contents" : update_post.contents,
            "created_at" : update_post.created_at
        }
            
        return JsonResponse({
            'status' : 200,
            'message' : '게시글 수정 성공',
            'result' : update_post_json
        })                
    else:
        return None
  
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):
    def get(self, request, title):
        post = get_object_or_404(Post, title = title)
        serializers = PostSerializer(post)
        return Response(serializers.data)
    
    def patch(self, request, title):
        post = get_object_or_404(Post, title = title)
        serializers = PostSerializer(post, data=request.data) 
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, title):
        post = get_object_or_404(Post, title = title)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 오류 처리
    
def handler404(request, exception):
    return JsonResponse({
        'status' : 404,
        'message' : '404 Not Found Error',
        'result' : None
    })