from django.contrib.auth.models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    This serializer handles user registration by validating the 
    provided data, ensuring that passwords match and that the 
    email is unique. It also creates a new User instance if all
    validations pass.

    Attributes:
        fullname (CharField): Full name of the user. Write-only.
        repeated_password (CharField): Confirmation of the password. Write-only.

    Meta:
        model (User): The User model from Django auth.
        fields (list): Fields to be serialized ('fullname', 'email', 'password', 'repeated_password').
        extra_kwargs (dict): Ensures 'password' is write-only.
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
        """
        Creates a new User instance after validating input data.

        Validations:
            - Password and repeated_password must match.
            - Email must be unique.

        Raises:
            serializers.ValidationError: If passwords do not match or email already exists.

        Returns:
            User: The newly created User instance.
        """
        password = self.validated_data['password']
        repeated_password = self.validated_data['repeated_password']
        email = self.validated_data['email']
        fullname = self.validated_data['fullname']

        if password != repeated_password:
            raise serializers.ValidationError(
                {'Error': "Passwords don't match"})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'Error': 'User with this email already exists'})

        account = User(
            email=email,
            username=email,
            first_name=fullname
        )

        account.set_password(password)
        account.save()
        return account
