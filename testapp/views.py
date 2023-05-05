from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.core import serializers
import json
from .models import Test

# Create your views here.
@require_http_methods(["GET"])     
def get_testdata_all(request):
    
    testdata_obj = Test.objects.all()

    testdata_list = []

    for test in testdata_obj:

        test_data = {
            "id" : test.pk,
            "title" : test.title,
            "content" : test.content,
            "created_at" : test.created_at,
        }        

        testdata_list.append(test_data) 
        
    return JsonResponse({
        'status' : 200,
        'message' : '게시글 조회 성공',
        'data' : testdata_list,
    })
    
@require_http_methods(["GET"])
def get_testdata(request, id):
    testdata_all = Test.objects.filter(id = id)
    
    testdata_json_list = []
    
    for testdata in  testdata_all:
        testdata_json = {
            "title" : testdata.title,
            "content" : testdata.content
        }
        
        testdata_json_list.append(testdata_json)
        
    return JsonResponse({
        'status' : 200,
        "message" : '게시글 조회 성공',
        'data' : testdata_json_list
    })

@require_http_methods(['POST'])    
def create_testdata(request):
    body = json.loads(request.body.decode('utf-8'))
    
    new_testdata = Test.objects.create(
           title = body['title'],
           content = body['content'],
       )
    
    new_testdata_json = {
           "id" : new_testdata.id,
           "titie" : new_testdata.title,
           "content" : new_testdata.content,
           "created_at" : new_testdata.created_at,
       }
    
    return JsonResponse({
        'status' : 200,
        'message' : '게시글 생성 성공',
        'data' : new_testdata_json
    })