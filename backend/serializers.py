from rest_framework.serializers import ModelSerializer
from backend.models import UserDetail, Tag, TagDetail, Video, PlaylistVideo, ViewHistory, Comment, Challenge
from django.db import models
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.registration.views import RegisterView
from django.views.decorators.csrf import csrf_exempt





class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class PermissionSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['is_active', 'is_staff', 'is_superuser']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'image', 'first_name', 'last_name', 'email', 'is_staff']

class UserDetailSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserDetail
        fields = '__all__'


class UserDetailViewSerializer(ModelSerializer):
    class Meta:
        model = UserDetail
        fields = '__all__'


class UserViewSerializer(ModelSerializer):
    userdetail = UserDetailViewSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'userdetail']



class TagDetailSerializer(ModelSerializer):
    class Meta:
        model = TagDetail
        fields = '__all__'


class TagSerializer(ModelSerializer):
    tag_detail = serializers.SerializerMethodField('_get_children')

    def _get_children(self, obj):
        serializer = TagDetailSerializer(obj.tagdetail_set.all(), many=True)
        return serializer.data

    class Meta:
        model = Tag
        fields = ['id', 'name', 'tag_detail']


class VideoSerializer(ModelSerializer):
    # tag_type = TagDetailSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Video
        fields = '__all__'

class VideoViewSerializer(ModelSerializer):
    tag_type = TagDetailSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Video
        fields = '__all__'


class VideoSerializerUpdate(ModelSerializer):
    class Meta:
        model = Video
        fields = ['name', 'description', 'tag_type', 'image']



class PlaylistVideoSerializerView(ModelSerializer):
    video = VideoSerializer(read_only=True, many=True)
    class Meta:
        model = PlaylistVideo
        fields = '__all__'

class PlalistVideoSerializer(ModelSerializer):
    class Meta:
        model = PlaylistVideo
        fields = '__all__'

class PlaylistVideoSerializerUpdate(ModelSerializer):
    class Meta:
        model = PlaylistVideo
        fields = ['name', 'image', 'description']


class ViewHistorySerializer(ModelSerializer):
    video = VideoSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = ViewHistory
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ChallengeSerializer(ModelSerializer):
    comment = CommentSerializer(read_only=True)

    class Meta:
        model = Challenge
        fields = '__all__'
