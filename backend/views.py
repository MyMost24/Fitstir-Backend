from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.contrib import admin
import json
import base64
import uuid


from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import VideoSerializer, TagSerializer, PlaylistVideoSerializer, TagDetailSerializer, UserDetailSerializer, UserSerializer,\
    ViewHistorySerializer, ChallengeSerializer, CommentSerializer, VideoViewSerializer

from .models import Video, Tag, PlaylistVideo, TagDetail, UserDetail, Comment, Challenge, ViewHistory



def convertImagetofile(img):
    format, imgstr = img.split(';base64,')
    ext = format.split('/')[-1]
    image_name = str(uuid.uuid4()) + "."+ext
    return ContentFile(base64.b64decode(imgstr), image_name)



class VideoViewset(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoViewSerializer

class VideoAPIView(APIView):
    def get(self, request,pk, format=None):
        return Response({"hello":pk})
    
    def post(self, request, format=None):
        tags = list(map(int, request.data.get('tag_type').split(',')))
        form = {
            "tag_type": tags,
            "name": request.data.get('name'),
            "image": request.data.get('image'),
            "description": request.data.get('description'),
            "video": request.data.get('video'),
        }

        serializer = VideoSerializer(data=form)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    
 
class TagViewset(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagDetailViewset(viewsets.ModelViewSet):
    queryset = TagDetail.objects.all()
    serializer_class =  TagDetailSerializer

class PlaylistVideoViewset(viewsets.ModelViewSet):
    queryset = PlaylistVideo.objects.all()
    serializer_class = PlaylistVideoSerializer

class UserDetailViewset(viewsets.ModelViewSet):
    queryset = UserDetail.objects.all()
    serializer_class = UserDetailSerializer

class UserViewser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class ChallengeViewset(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer

class ViewHistoryViewset(viewsets.ModelViewSet):
    queryset = ViewHistory.objects.all()
    serializer_class = ViewHistorySerializer