from rest_framework import serializers
from .models import *

class PostSerializer(serializers.ModelSerializer):
    contents = serializers.CharField(trim_whitespace=False)
    
    class Meta:
        model = Post
        fields = "__all__"
        
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"  
        
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        field = "__all__"