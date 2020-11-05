from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from simple_history.admin import SimpleHistoryAdmin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, inlines
from backend.models import Tag, Video, TagDetail, UserDetail, Challenge, PlaylistVideo, Comment, InPlaylist, \
    InChallenge, \
    InVideoChallenge, VideoChallenge


class VideoAdmin(admin.ModelAdmin):
    filter_horizontal = ['tag_type']


class TagDetailInline(admin.TabularInline):
    model = TagDetail


class TagAdmin(admin.ModelAdmin):
    inlines = [
        TagDetailInline
    ]


class UserdetailInline(admin.StackedInline):
    model = UserDetail
    can_delete = False
    verbose_name = 'UserDetail'


class UserAdmin(UserAdmin):
    inlines = (UserdetailInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class PlaylistVideoAdmin(admin.ModelAdmin):
    filter_horizontal = ['video']


class TagDetailAdmin(admin.ModelAdmin):
    list_display = ['name', 'detail']


class VideoChallengeInline(admin.TabularInline):
    model = VideoChallenge

class CommentInline(admin.TabularInline):
    model = Comment


class ChallengeAdmin(admin.ModelAdmin):
    inlines = [
        VideoChallengeInline
    ]

class VideoChallengeAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline
    ]


admin.site.register(PlaylistVideo, PlaylistVideoAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(UserDetail, SimpleHistoryAdmin)
admin.site.register(TagDetail, TagDetailAdmin)
admin.site.register(Comment)
admin.site.register(InPlaylist)
admin.site.register(InChallenge)
admin.site.register(VideoChallenge, VideoChallengeAdmin)
admin.site.register(InVideoChallenge)
