from rest_framework import serializers
from accounts.models import *
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _

class ProfileSerializer(serializers.ModelSerializer):
    # posts_count = serializers.ReadOnlyField()
    # followers_count = serializers.ReadOnlyField()
    # following_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Profile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'profile']


class VisitedUserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)
    class Meta:
        model = User
        fields = ['id', 'profile']

class RegisterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                _('Your old password was entered incorrectly. Please enter it again.')
            )
        return value

    def validate(self, data):
        if not data['new_password']:
            raise serializers.ValidationError({'new_password': _("Musisz podac nowe hasło")})
        if data['new_password'] == data['old_password']:
            raise serializers.ValidationError({'new_password': _("Nowe i stare hasło nie mogą być takie same")})
        password_validation.validate_password(data['new_password'], self.context['request'].user)
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user


