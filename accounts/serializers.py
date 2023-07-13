from rest_framework import serializers
from .models import Member
from rest_framework_simplejwt.serializers import RefreshToken

class ResisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)
    email = serializers.CharField(required = True)
    name = serializers.CharField(required = True)
    
    class Meta:
        model = Member
        fields = ['id', 'username', 'password', 'email', 'name']
        
    # 회원 정보 저장    
    def save(self, request):
        
        member = Member.objects.create(
            username = self.validated_data['username'],
            email = self.validated_data['email'],
            name = self.validated_data['name'],
        )
        
        # password는 별도로 암호화
        member.set_password(self.validated_data["password"])
        
        member.save()
        
        return member
    
    # 중복 회원 가입 검사
    def validate(self, data):
        username = data.get("username", None)
        
        if Member.objects.filter(username = username).exists():
            raise serializers.ValidationError('username already exists')
        
        return data
    
class AuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    
    class Meta:
        model = Member
        fields = ["username", "password"]
        
    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        
        if Member.objects.filter(username=username).exists():
            member = Member.objects.get(username=username)
              
            if not member.check_password(password):
                raise serializers.ValidationError("wrong password")
        else:
            raise serializers.ValidationError("member account not exist")
		        
        token = RefreshToken.for_user(member)
        refresh_token = str(token)
        access_token = str(token.access_token)
		
        data = {
				'member':member,
				'refresh_token':refresh_token,
				'access_token':access_token,
		}
		
        return data