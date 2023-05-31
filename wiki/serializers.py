from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    contents = serializers.CharField(trim_whitespace=False)
    class Meta:
        model = Post
        fields = "__all__"    