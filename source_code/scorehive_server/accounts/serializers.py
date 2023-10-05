import re

from django.core.validators import (EmailValidator, MaxLengthValidator,
                                    RegexValidator)
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            MaxLengthValidator(100),
            EmailValidator,
            UniqueValidator(queryset=User.objects.all()),
        ]
    )

    def validate_name(self, name):
        if len(name) > 100 or len(name) < 2:
            raise serializers.ValidationError("Name should be between 2-100 characters")
        regex = r"^[a-zA-Z ]*$"
        if not re.match(regex, name):
            raise serializers.ValidationError("Name should have only alphabets")
        return name

    phone_number = serializers.CharField(
        validators=[
            RegexValidator(
                regex="^[+][0-9]{1,3}[ ][0-9]{10}$",
                message="Phone number should be in +999 9999999999 format",
            ),
            UniqueValidator(queryset=User.objects.all()),
        ]
    )

    password = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[!#$%&'()*+,-./:;<=>?@[\]^_`{|}~]).{8,20}$",
                message="Invalid password",
            )
        ]
    )

    class Meta:
        model = User
        fields = ("email", "name", "phone_number", "password")


class UserDetailsUpdateSerializer(serializers.ModelSerializer):
    def validate_name(self, name):
        if len(name) > 100 or len(name) < 2:
            raise serializers.ValidationError("Name should be between 2-100 characters")
        regex = r"^[a-zA-Z ]*$"
        if not re.match(regex, name):
            raise serializers.ValidationError("Name should have only alphabets")
        return name

    phone_number = serializers.CharField(
        validators=[
            RegexValidator(
                regex="^[+][0-9]{1,3}[ ][0-9]{10}$",
                message="Phone number should be in +999 9999999999 format",
            ),
            UniqueValidator(queryset=User.objects.all()),
        ]
    )

    class Meta:
        model = User
        fields = ("name", "phone_number")


class SearchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "email")
