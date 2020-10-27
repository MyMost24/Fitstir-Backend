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

from .serializers import VideoSerializer, TagSerializer, PlaylistVideoSerializer, TagDetailSerializer, \
    UserDetailSerializer, UserSerializer, ViewHistorySerializer, ChallengeSerializer, CommentSerializer,\
    VideoViewSerializer, VideoSerializerUpdate, VideoSerializerUpdateView, PermissionSerializer,\
    PlaylistVideoSerializerUpdate, UserTestSerializer

from .models import Video, Tag, PlaylistVideo, TagDetail, UserDetail, Comment, Challenge, ViewHistory

class Permission(APIView):
    def get(self, request,id, format=None):
        try:
            item = User.objects.get(pk=id)
            serializer = PermissionSerializer(item)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=404)
        return Response({"hello":"asd"})


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailViewset(viewsets.ModelViewSet):
    queryset = UserDetail.objects.all()
    serializer_class = UserDetailSerializer


class UserTestViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserTestSerializer


def convertImagetofile(img):
    format, imgstr = img.split(';base64,')
    ext = format.split('/')[-1]
    image_name = str(uuid.uuid4()) + "." + ext
    return ContentFile(base64.b64decode(imgstr), image_name)


class VideoViewset(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoViewSerializer


class VideoAPIView(APIView):
    def get(self, request, pk, format=None):
        return Response({"hello": pk})

    def post(self, request, format=None):
        tags = list(map(int, request.data.get('tag_type', ).split(',')))
        form = {
            "tag_type": tags,
            "name": request.data.get('name', ),
            "image": request.data.get('image', ),
            "description": request.data.get('description', ),
            "video": request.data.get('video', ),
        }

        serializer = VideoSerializer(data=form)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class VideoAPIViewUpdate(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, pk, format=None):
        try:
            item = Video.objects.get(pk=pk)
            serializer = VideoSerializer(item)
            return Response(serializer.data)
        except Video.DoesNotExist:
            return Response(status=404)

    @csrf_exempt
    def put(self, request, pk, format=None):
        request.data['image'] = convertImagetofile(request.data.get('image'))
        try:
            item = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response(status=404)
        serializer = VideoSerializerUpdate(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, format=None):
        try:
            item = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class PlaylistVideoViewset(viewsets.ModelViewSet):
    queryset = PlaylistVideo.objects.all()
    serializer_class = PlaylistVideoSerializer


class PlaylistVideoAPIView(APIView):
    def get(self, request, pk, format=None):
        return Response({"hello": pk})

    def post(self, request, format=None):
        form = {
            "name": request.data.get('name', ),
            "image": request.data.get('image', ),
            "description": request.data.get('description', ),
        }

        serializer = PlaylistVideoAPIViewUpdate(data=form)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PlaylistVideoAPIViewUpdate(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, pk, format=None):

        try:
            item = PlaylistVideo.objects.get(pk=pk)
            serializer = PlaylistVideoSerializerUpdate(item)
            return Response(serializer.data)
        except PlaylistVideo.DoesNotExist:
            return Response(status=404)

    @csrf_exempt
    def put(self, request, pk, format=None):
        request.data['image'] = convertImagetofile(request.data.get('image'))
        try:
            item = PlaylistVideo.objects.get(pk=pk)
        except PlaylistVideo.DoesNotExist:
            return Response(status=404)
        serializer = PlaylistVideoSerializerUpdate(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, format=None):
        try:
            item = PlaylistVideo.objects.get(pk=pk)
        except PlaylistVideo.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class TagViewset(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagDetailViewset(viewsets.ModelViewSet):
    queryset = TagDetail.objects.all()
    serializer_class = TagDetailSerializer

class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ChallengeViewset(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer


class ViewHistoryViewset(viewsets.ModelViewSet):
    queryset = ViewHistory.objects.all()
    serializer_class = ViewHistorySerializer



