from rest_framework import serializers
from .models import *

class PostSerializer(serializers.ModelSerializer):
    contents = serializers.CharField(trim_whitespace=False)
    
    class Meta:
        model = Post
        fields = "__all__"
        
    def validate(self, data):
        title = data.get("title", None)
        
        if Post.objects.filter(title=title).exists():
            raise serializers.ValidationError('이미 존재하는 게시글 입니다.')
        
        return data
        
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"  
        
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        field = "__all__"