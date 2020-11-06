from django.urls import path, include
from django.conf.urls import include, url
from rest_framework import routers
from backend import views

# Create a router and register our viewsets with it.

router = routers.DefaultRouter()

router.register('videos', views.VideoViewset)
router.register('tag', views.TagViewset)
router.register('tagdetail', views.TagDetailViewset)
router.register('playlists', views.PlaylistVideoViewset)
router.register('userdetail', views.UserDetailViewViewset)
router.register('challenges', views.ChallengeViewset)




# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', views.AdminAPIView.as_view()),
    path('changetoadmin/', views.ChangeToAdmin.as_view()),
    path('user/', views.UserAPIView.as_view()),
    path('user/<int:pk>', views.UserUpdateAPIView.as_view()),
    path('userprofile/', views.UserProfileAPIView.as_view()),
    path('userprofile/<int:pk>', views.UserProfileAPIViewUpdate.as_view()),
    path('profile/password/<id>/', views.ChangePassword.as_view(), name='ChangePassword'),
    path('change/password/', views.UpdatePassword.as_view(), name='all_profile'),
    path('video', views.VideoAPIView.as_view()),
    path('video/<int:pk>', views.VideoAPIViewUpdate.as_view()),
    path('videobytag/<int:pk>', views.VideoByTagAPIView.as_view()),
    path('playlist/', views.PlaylistVideoCreateAPIView.as_view()),
    path('playlist/<int:pk>', views.PlaylistVideoAPIViewUpdate.as_view()),
    path('videoplaylist/', views.PlaylistAPIView.as_view()),
    path('videoplaylist/<int:pk>', views.InPlaylistAPIViewUpdeta.as_view()),
    path('userplaylist/<int:pk>', views.PlaylistVideoGetByUserIdAPIView.as_view()),
    path('adminplaylist/', views.PlaylistVideoGetByStaffAPIView.as_view()),
    path('challenge/', views.ChallengeAPIView.as_view()),
    path('challenge/<int:pk>', views.ChallengeAPIViewUpdate.as_view()),
    path('videochallenge/', views.VideoChallengeAPIView.as_view()),
    path('videochallenge/<int:pk>', views.VideoChallengeAPIView.as_view()),
    path('inchallenge/', views.InChallengeAPIView.as_view()),
    path('inchallenge/<int:pk>', views.InChallengeAPIViewUpdeta.as_view()),
    path('invideochallenge/', views.InVideoChallengeAPIView.as_view()),
    path('invideochallenge/<int:pk>', views.InVideoChallengeAPIViewUpdeta.as_view()),



    # path('videos', views.VideoAPIListView.as_view()),

]
