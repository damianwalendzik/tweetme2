from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL

class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
 
# Create your models here.
class Tweet(models.Model):
    #id = models.AutoField(primary_key=True)
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='tweet_user', blank=True, through=TweetLike)
    content = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to='images/',blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)



    #def __str__(self):
     #   return self.content
    
    class Meta:
        ordering = ['-id']
    @property
    def is_retweet(self):
        return self.parent != None
    def serialize(self):
        return {
            "id" : self.id,
            "content" : self.content,
            "likes" : 0,
             
        }