from rest_framework.serializers import ModelSerializer
from backend.models import UserDetail, Tag, TagDetail, Video, PlaylistVideo, ViewHistory, Comment, Challenge
from django.db import models
from rest_framework import serializers
from django.contrib.auth.models import User


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = UserDetail
        fields = '__all__'


class UserSerializer(ModelSerializer):
    userdetail = UserDetailSerializer(read_only=True)

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
        fields = ['title', 'description', 'tags']


class VideoSerializerUpdateView(ModelSerializer):
    class Meta:
        model = Video
        fields = ['title', 'description', 'tags', 'image']


class PlaylistVideoSerializer(ModelSerializer):
    video = VideoSerializer(read_only=True, many=True)
    class Meta:
        model = PlaylistVideo
        fields = '__all__'



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
