from django.contrib.auth.models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.

    Validates password confirmation and ensures email uniqueness.
    """
    fullname = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def save(self):
        password = self.validated_data['password']
        repeated_password = self.validated_data['repeated_password']
        email = self.validated_data['email']
        fullname = self.validated_data['fullname']

        if password != repeated_password:
            raise serializers.ValidationError(
                {'Error': "Passwords don't match."})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'Error': 'User with this email already exists.'})

        account = User(
            email=email,
            username=email,
            first_name=fullname
        )

        account.set_password(password)
        account.save()
        return account


class CustomLoginEmailOnlySerializer(serializers.Serializer):
    """
    Authenticates a user by email and password.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {'Error': "User doesn't exist."})

        if not user.check_password(password):
            raise serializers.ValidationError(
                {'Error': 'Wrong password'})

        # Add the authenticated user to validated data
        data['user'] = user
        return data
