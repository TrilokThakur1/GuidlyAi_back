from rest_framework import serializers
from .models import registerModal

class RegisterSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)  # Useful to return the MongoDB ID
    name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)  # Protects the password from being sent back
    
    # Keeps it flexible so users don't HAVE to upload a photo immediately
    avatar = serializers.FileField(required=False, allow_null=True)
    avatar_url = serializers.SerializerMethodField()

    def get_avatar_url(self, obj):
        """
        Converts the Cloudinary object from MongoDB into a fully qualified HTTPS URL 
        for your React frontend.
        """
        # If 'obj' is a dictionary (common in some raw MongoDB setups)
        if isinstance(obj, dict):
            avatar_data = obj.get('avatar')
            # If it's already a Cloudinary URL string or object with a url attribute
            if hasattr(avatar_data, 'url'):
                return avatar_data.url
            return avatar_data if isinstance(avatar_data, str) else None
            
        # If 'obj' is a standard Django model instance
        if hasattr(obj, 'avatar') and obj.avatar:
            return obj.avatar.url
            
        return None

    def create(self, validated_data):
        """
        Handles saving the user data into MongoDB via your registerModal.
        """
        return registerModal.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    
class UserIdSerializer(serializers.Serializer):
    userId = serializers.CharField()