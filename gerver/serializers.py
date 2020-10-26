from .models import Group, Post, Profile
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    """
    This is used by ProfileSerializer to serialize
    nested user object.
    Example:
        user:{
            "email",
            "username",
            "first_name",
            "last_name",
            "password"
        }
    """
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return User(**validated_data)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name' ,'password']
        extra_kwargs = {'password': {'write_only': True}}

class ProfileSerializer(serializers.ModelSerializer):
    """
    Example:
        {
            user: {
                "email",
                "username",
                "first_name",
                "last_name",
                "password",
            }
            group_id: {
                "id"
            }
            ...
        }
    """
    user = UserSerializer()

    def create(self, validated_data):
        user = User(
            email=validated_data['user']['email'],
            username=validated_data['user']['username']
        )
        user.set_password(validated_data['user']['password'])
        user.save()
        return Profile.objects.create(user=user)

    class Meta:
        model = Profile
        fields = ['user']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['user', 'group', 'date_time', 'post_text', 'post_image']


