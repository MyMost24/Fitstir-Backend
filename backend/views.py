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
    CommentSerializer, ChangePasswordSerializer, UserViewSerializer, UserDetailViewSerializer, \
    UserDetailSerializer, UserSerializer, UserUpdateSerailizer, CommentSerializerView, CommentSerializer, \
    ChallengeSerializer, ChallengeViewSerializer, VideoChallengeSerializer, VideoChallengeViewSerializer, \
    InChallengeSerializer, InVideoChallengeSerializer, InVideoChallengeViewSerializer, InChallengeViewSerializer

from .models import Video, Tag, PlaylistVideo, TagDetail, UserDetail, Comment, Challenge, InPlaylist, InChallenge, VideoChallenge, InVideoChallenge


def convertImagetofile(img):
    format, imgstr = img.split(';base64,')
    ext = format.split('/')[-1]
    image_name = str(uuid.uuid4()) + "." + ext
    return ContentFile(base64.b64decode(imgstr), image_name)


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


class AdminAPIView(APIView):
    def get(self, request, format=None):
        items = User.objects.filter(is_staff=True)
        serializer = UserViewSerializer(items, many=True)
        return Response(serializer.data)


class ChangeToAdmin(APIView):
    def post(self, request, format=None):
        user = User.objects.get(request.data.get('user'))
        user.is_staff = True
        user.is_active = False
        user.save()
        return Response({"success": "GG"})


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

class UserProfileAPIView(APIView):
    def post(self, request, format=None):
        form = {

            "name": request.data.get('name', ),
            "birthday": request.data.get('birthday', ),
            "phone_number": request.data.get('phone_number', ),
            "address": request.data.get('address', ),
            "high": request.data.get('high', ),
            "weight": request.data.get('weight', ),
            "bmi": request.data.get('bmi', ),
            "user": request.data.get('user', ),

        }
        serializer = UserDetailSerializer(data=form)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class UserProfileAPIViewUpdate(APIView):
    def get(self, request, pk, format=None):
        try:
            item = UserDetail.objects.filter(user=pk)
            serializer = UserDetailSerializer(item)
            return Response(serializer.data)
        except UserDetail.DoesNotExist:
            return Response(status=404)

    def put(self, request, pk, format=None):
        try:
            item = UserDetail.objects.get(pk=pk)
        except UserDetail.DoesNotExist:
            return Response(status=404)
        serializer = UserDetailSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)



class UserDetailViewViewset(viewsets.ModelViewSet):
    queryset = UserDetail.objects.all()
    serializer_class = UserDetailViewSerializer


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
        tags = list(map(int, request.data.get('tag_type', ).split(',')))
        form = {
            "tag_type": tags,
            "name": request.data.get('name', ),
            "image": request.data.get('image', ),
            "description": request.data.get('description', ),

        }
        try:
            item = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response(status=404)
        serializer = VideoSerializerUpdate(item, data=form)
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
            serializer = InPlaylistSeializerView(item, many=True)
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


class ChallengeViewset(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeViewSerializer

class ChallengeAPIView(APIView):

    def post(self, request, format=None):
        form = {
            "name": request.data.get('name', ),
            "description": request.data.get('description', ),
            "image": request.data.get('image', ),
            "user": request.data.get('user', ),
        }
        serializer = ChallengeSerializer(data=form)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class ChallengeAPIViewUpdate(APIView):
    def get(self, request, pk, format=None):
        try:
            item = Challenge.objects.get(pk=pk)
            serializer = ChallengeSerializer(item)
            return Response(serializer.data)
        except PlaylistVideo.DoesNotExist:
            return Response(status=404)

    def put(self, request, pk, format=None):
        try:
            item = Challenge.objects.get(pk=pk)
        except Challenge.DoesNotExist:
            return Response(status=404)
        serializer = ChallengeSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, format=None):
        try:
            item = Challenge.objects.get(pk=pk)
        except Challenge.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)

class VideoChallengeAPIView(APIView):
    def get(self, request, format=None):
        item = VideoChallenge.objects.all()
        serializer = VideoChallengeViewSerializer(item, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        form = {
            "description": request.data.get('description', ),
            "video": request.data.get('video', ),
            "image": request.data.get('image', ),
            "challenge": request.data.get('challenge', ),
            "user": request.data.get('user', ),
        }
        serializer = VideoChallengeSerializer(data=form)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class VideoChallengeAPIViewUpdate(APIView):
    def get(self, request, pk, format=None):
        try:
            item = VideoChallenge.objects.get(pk=pk)
            serializer = VideoChallengeViewSerializer(item)
            return Response(serializer.data)
        except PlaylistVideo.DoesNotExist:
            return Response(status=404)

    def put(self, request, pk, format=None):
        try:
            item = VideoChallenge.objects.get(pk=pk)
        except VideoChallenge.DoesNotExist:
            return Response(status=404)
        serializer = VideoViewSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, format=None):
        try:
            item = VideoChallenge.objects.get(pk=pk)
        except VideoChallenge.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)

class InChallengeAPIView(APIView):
    def get(self, request, format=None):
        item = InChallenge.objects.all()
        serializer = InChallengeSerializer(item, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        form = {
            "video": request.data.get('video', ),
            "playlist": request.data.get('playlist', ),
        }
        serializer = InChallengeSerializer(data=form)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class InChallengeAPIViewUpdeta(APIView):
    def get(self, request, pk, format=None):
        try:
            item = InChallenge.objects.filter(challenge=pk)
            serializer = InChallengeViewSerializer(item, many=True)
            return Response(serializer.data)
        except InPlaylist.DoesNotExist:
            return Response(status=404)

    def delete(self, request, pk, format=None):

        try:
            item = InChallenge.objects.get(pk=pk)
        except InPlaylist.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class InChallengeAPIView(APIView):
    def get(self, request, format=None):
        item = InChallenge.objects.all()
        serializer = InChallengeSerializer(item, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        form = {
            "video": request.data.get('video', ),
            "playlist": request.data.get('playlist', ),
        }
        serializer = InChallengeSerializer(data=form)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class InChallengeAPIViewUpdeta(APIView):
    def get(self, request, pk, format=None):
        try:
            item = InChallenge.objects.filter(challenge=pk)
            serializer = InChallengeViewSerializer(item, many=True)
            return Response(serializer.data)
        except InPlaylist.DoesNotExist:
            return Response(status=404)

    def delete(self, request, pk, format=None):

        try:
            item = InChallenge.objects.get(pk=pk)
        except InChallenge.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class InVideoChallengeAPIView(APIView):
    def get(self, request, format=None):
        item = InVideoChallenge.objects.all()
        serializer = InVideoChallengeSerializer(item, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        form = {
            "video": request.data.get('video', ),
            "user": request.data.get('user', ),
        }
        serializer = InVideoChallengeSerializer(data=form)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class InVideoChallengeAPIViewUpdeta(APIView):
    def get(self, request, pk, format=None):
        try:
            item = InVideoChallenge.objects.filter(challenge=pk)
            serializer = InVideoChallengeViewSerializer(item, many=True)
            return Response(serializer.data)
        except InPlaylist.DoesNotExist:
            return Response(status=404)

    def delete(self, request, pk, format=None):

        try:
            item = InVideoChallenge.objects.get(pk=pk)
        except InVideoChallenge.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)




# class ViewHistoryViewset(viewsets.ModelViewSet):
#     queryset = ViewHistory.objects.all()
#     serializer_class = ViewHistorySerializer
