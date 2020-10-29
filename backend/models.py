from django.contrib.auth.models import User
from django.db import models
from simple_history.models import HistoricalRecords
from polymorphic.models import PolymorphicModel


class UserDetail(models.Model):
    image = models.FileField(upload_to='user/', null=True, blank=True)
    birthday = models.DateField()
    phone_number = models.CharField(max_length=15,)
    address = models.TextField(max_length=255)
    high = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bmi = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    # history = HistoricalRecords()
    user = models.OneToOneField(User, on_delete=models.CASCADE,)

    def __str__(self):
        return '{},{}'.format(self.user.username, self.birthday)



class Tag(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return '{}'.format(self.name)
    class Meta:
        unique_together = ('name',)

class TagDetail(models.Model):
    name = models.CharField(max_length=255)
    detail = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '{}'.format(self.name)

class Video(models.Model):
    image = models.FileField(upload_to='images/', null=True, blank=True, verbose_name="Image")
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=5500, null=True, blank=True, default='Video is not description.')
    video = models.FileField(upload_to='videos/', null=True, blank=True, verbose_name="Video File")
    tag_type = models.ManyToManyField(TagDetail)

    def __str__(self):
        return '{},{}'.format(self.name, self.tag_type)


class PlaylistVideo(models.Model):
    image = models.FileField(upload_to='images', null=True, verbose_name="Playlist Image")
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=5500, null=True, blank=True, default='None description.')
    video = models.ManyToManyField(Video, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.name)


# class ViewHistory(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     video = models.ForeignKey(Video, on_delete=models.CASCADE)
#     create_at = models.DateTimeField(auto_now_add=True)



class Challenge(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2500, null=True, blank=True, default='No description')
    image = models.FileField(upload_to='challenge_image', verbose_name='Challenge Image',null=True, blank=True)
    video = models.FileField(upload_to='challenge_video', verbose_name='Challenge Video', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    def __str__(self):
        return '{}'.format(self.name)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    commentText = models.CharField(max_length=500, null=True, blank=True, default='Comment')
    commentVideo = models.FileField(upload_to='challenge_videos', null=True, blank=True)
    commentImage = models.FileField(upload_to='challenge_video_image', null=True, blank=True)

    def __str__(self):
        return '{},{},{}'.format(self.user.username, self.challenge, self.commentText)

class InPlaylist(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    playlist = models.ForeignKey(PlaylistVideo, on_delete=models.CASCADE)
