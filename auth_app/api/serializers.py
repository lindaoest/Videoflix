from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

# Serializer for user registration
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

    # Custom validation to check password match and existing email
    def validate(self, data):
        pw = data['password']
        repeated_pw = data['confirmed_password']

        if pw != repeated_pw:
            raise serializers.ValidationError({'message': 'Passwords do not match'})

        if User.objects.filter(email=data['email']):
            raise serializers.ValidationError({'message': 'This email already exists'})

        return data

    # Create a new user instance with hashed password
    def create(self, validated_data):
        user = User(username=validated_data['email'], email=validated_data['email'])
        # Hash the password before saving
        user.set_password(validated_data['password'])
        user.save()

        return user

# Use the custom user model
User = get_user_model()

# Serializer for user login using JWT
class LoginSerializer(TokenObtainPairSerializer):
    # Email is required
    email = serializers.EmailField(required=True)
    # Password is write-only to avoid exposure in responses
    password = serializers.CharField(write_only=True, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove the default 'username' field from JWT serializer
        if 'username' in self.fields:
            self.fields.pop('username')

    # Custom validation to authenticate user with email and password
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

        # Generate token pair using the username field and password
        token_data = super().validate({
            self.username_field: user.username,
            'password': password
        })

        # Include additional user data in the response
        token_data['username'] = user.username
        token_data['pk'] = user.id

        return token_data

# Serializer to confirm and set a new password
class ConfirmPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    # Validate that the new password and confirmation match
    def validate(self, data):
        pw = data['new_password']
        repeated_pw = data['confirm_password']

        if pw != repeated_pw:
            raise serializers.ValidationError({'message': 'Passwords do not match'})

        return data

    # Set the new password for the user
    def create(self, validated_data):
        user = self.context['user']
        # Hash the password before saving
        user.set_password(validated_data['new_password'])
        user.save()

        return user

