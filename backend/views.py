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
from rest_framework.permissions import IsAuthenticated

from .serializers import VideoSerializer, VideoViewSerializer, VideoSerializerUpdate, \
    TagSerializer, TagDetailSerializer, PlaylistVideoSerializerUpdate, PlaylistVideoSerializerView, \
    PlaylistVideoSerializer, InPlaylistSerializer, InPlaylistSeializerView, \
    ChallengeSerializerView, CommentSerializer, ChangePasswordSerializer, \
    UserViewSerializer, UserDetailViewSerializer, UserDetailSerializer, UserSerializer, \
    UserUpdateSerailizer, InChallengeSerailizer, InChallengeSerializerView

from .models import Video, Tag, PlaylistVideo, TagDetail, UserDetail, Comment, Challenge, InPlaylist, InChallenge


class ChangePassword(APIView):
    def put(self, request, pk, format=None):
        password = request.data.get('new_password')
        u = User.objects.get(pk=pk)
        u.set_password(password)
        u.save()
        return Response({"password": "Success"})


class UpdatePassword(APIView):
    """
    An endpoint for changing password.
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=400)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=204)

        return Response(serializer.errors, status=400)


class UserAPIView(APIView):
    def get(self, request, format=None):
        items = User.objects.filter(is_active=True, is_staff=False)
        serializer = UserViewSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        form = {
            "first_name": request.data.get('first_name', ),
            "last_name": request.data.get('last_name', ),
            "email": request.data.get('email', ),
            "username": request.data.get('username', ),
            "password": request.data.get('password', ),
            "is_active": request.data.get('is_active', ),
        }
        serializer = UserSerializer(data=form)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UserUpdateAPIView(APIView):
    def get(self, request, pk, format=None):
        try:
            item = User.objects.get(pk=pk)
            serializer = UserUpdateSerailizer(item)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=404)

    @csrf_exempt
    def put(self, request, pk, format=None):
        try:
            item = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=404)
        serializer = UserUpdateSerailizer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, format=None):
        try:
            item = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class UserDetailViewViewset(viewsets.ModelViewSet):
    queryset = UserDetail.objects.all()
    serializer_class = UserDetailViewSerializer


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
    serializer_class = PlaylistVideoSerializerView


class PlaylistVideoGetByUserIdAPIView(APIView):
    def get(self, request, pk):
        items = PlaylistVideo.objects.filter(user=pk).order_by('pk')
        serializer = PlaylistVideoSerializerView(items, many=True)
        return Response(serializer.data)


class PlaylistVideoGetByStaffAPIView(APIView):
    def get(self, request):
        items = PlaylistVideo.objects.filter(user__is_staff=True)
        serializer = PlaylistVideoSerializerView(items, many=True)
        return Response(serializer.data)


class PlaylistVideoCreateAPIView(APIView):

    def post(self, request, format=None):
        form = {
            "name": request.data.get('name', ),
            "image": request.data.get('image', ),
            "description": request.data.get('description', ),
            "user": request.data.get('user', ),
        }

        serializer = PlaylistVideoSerializer(data=form)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PlaylistAPIView(APIView):

    def get(self, request, format=None):
        item = InPlaylist.objects.all()
        serializer = InPlaylistSeializerView(item, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        form = {
            "video": request.data.get('video', ),
            "playlist": request.data.get('playlist', ),
        }
        serializer = InPlaylistSerializer(data=form)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class InPlaylistAPIViewUpdeta(APIView):
    def get(self, request, pk, format=None):
        try:
            item = InPlaylist.objects.filter(playlist=pk)
            serializer = InPlaylistSeializerView(item)
            return Response(serializer.data)
        except InPlaylist.DoesNotExist:
            return Response(status=404)

    def delete(self, request, pk, format=None):

        try:
            item = InPlaylist.objects.get(pk=pk)
        except InPlaylist.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


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
        # request.data['image'] = convertImagetofile(request.data.get('image'))
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
    serializer_class = ChallengeSerializerView


class ChallengeAIPView(APIView):
    def get(self, request, format=None):
        item = InChallenge.objects.all()
        serializer = InChallengeSerializerView(item, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        form = {
            "comment": request.data.get('comnnet', ),
            "challenge": request.data.get('challenge', ),
        }
        serializer = InChallengeSerailizer(data=form)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class ChallengeAIPViewUpdate(APIView):
    def get(self, request, pk, format=None ):
        try:
            item = InChallenge.objects.get(challenge=pk)
            serializer = InChallengeSerializerView(item)
            return Response(serializer.data)
        except InChallenge.DoesNotExist:
            return Response(status=404)

    def delete(self, request, pk, format=None):

        try:
            item = InChallenge.objects.get(pk=pk)
        except InChallenge.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


# class ViewHistoryViewset(viewsets.ModelViewSet):
#     queryset = ViewHistory.objects.all()
#     serializer_class = ViewHistorySerializer
