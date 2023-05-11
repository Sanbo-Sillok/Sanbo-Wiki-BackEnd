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
            "contents" : test.contents,
            "created_at" : test.created_at
        }        

        testdata_list.append(test_data) 
        
    return JsonResponse({
        'status' : 200,
        'message' : '게시글 조회 성공',
        'result' : testdata_list
    })
    
@require_http_methods(["GET"])
def get_testdata(request, title):
    testdata = get_object_or_404(Test, title = title)
    
    testdata_json = {
        "id" : testdata.pk,
        "title" : testdata.title,
        "contents" : testdata.contents,
        "created_at" : testdata.created_at      
    }
    
    return JsonResponse({
            'status' : 200,
            'message' : '게시글 조회 성공',
            'result' : testdata_json
        })

@require_http_methods(["POST"])    
def create_testdata(request):
    body = json.loads(request.body.decode('utf-8'))
    
    new_testdata = Test.objects.create(
           title = body['title'],
           contents = body['contents'], 
       )
    
    new_testdata_json = {
           "id" : new_testdata.id,
           "title" : new_testdata.title,
           "contents" : new_testdata.contents,
           "created_at" : new_testdata.created_at
       }
    
    return JsonResponse({
        'status' : 200,
        'message' : '게시글 생성 성공',
        'result' : new_testdata_json
    })
    