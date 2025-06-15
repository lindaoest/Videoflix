from rest_framework import serializers
from django.contrib.auth.models import User

""" Serializer for user registration """
class RegistrationSerializer(serializers.ModelSerializer):
    # Email is required
    email = serializers.EmailField(required=True)
    # Password is write-only to avoid exposure in responses
    password = serializers.CharField(write_only=True, required=True)
    # Repeat password to confirm correctness
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'repeated_password']

    # Validate that password and repeated password match
    def validate(self, data):
        pw = data['password']
        repeated_pw = data['repeated_password']

        if pw != repeated_pw:
            raise serializers.ValidationError({'error': 'Passwörter stimmen nicht überein'})
        return data

    # Validate that the email does not already exist in the database
    def validate_email(self, value):
        if User.objects.filter(email=value):
            raise serializers.ValidationError({'error': 'Diese Email existiert bereits'})
        return value

    # Create a new user and associated profile based on profile type
    def create(self, validated_data):
        user = User(email=validated_data['email'])
        # Hash the password before saving
        user.set_password(validated_data['password'])
        user.save()

        return user