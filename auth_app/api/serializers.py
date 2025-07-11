from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

""" Serializer for user registration """
class RegistrationSerializer(serializers.ModelSerializer):
    # Email is required
    email = serializers.EmailField(required=True)
    # Password is write-only to avoid exposure in responses
    password = serializers.CharField(write_only=True, required=True)
    # Repeat password to confirm correctness
    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirmed_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # Validate that password and repeated password match
    # Check if email already exists
    def validate(self, data):
        pw = data['password']
        repeated_pw = data['confirmed_password']

        if pw != repeated_pw:
            raise serializers.ValidationError({'message': 'Passwords do not match'})

        if User.objects.filter(email=data['email']):
            raise serializers.ValidationError({'message': 'This email already exists'})

        return data

    # Create a new user and associated profile based on profile type
    def create(self, validated_data):
        user = User(username=validated_data['email'], email=validated_data['email'])
        # Hash the password before saving
        user.set_password(validated_data['password'])
        user.save()

        return user

User = get_user_model()

class LoginSerializer(TokenObtainPairSerializer):
    # Email is required
    email = serializers.EmailField(required=True)
    # Password is write-only to avoid exposure in responses
    password = serializers.CharField(write_only=True, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'username' in self.fields:
            self.fields.pop('username')

    def validate(self, data):
        email = data['email']
        password = data['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'message': 'The data entered is not correct'})

        if not user.check_password(password):
            raise serializers.ValidationError({'message': 'The data entered is not correct'})

        self.user = user

        token_data = super().validate({
            self.username_field: user.username,
            'password': password
        })

        token_data['username'] = user.username
        token_data['pk'] = user.id

        return token_data

class ConfirmPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    # Validate that password and repeated password match
    def validate(self, data):
        pw = data['new_password']
        repeated_pw = data['confirm_password']

        if pw != repeated_pw:
            raise serializers.ValidationError({'message': 'Passwords do not match'})

        return data

    # Create a new user and associated profile based on profile type
    def create(self, validated_data):
        user = self.context['user']
        # Hash the password before saving
        user.set_password(validated_data['new_password'])
        user.save()

        return user

