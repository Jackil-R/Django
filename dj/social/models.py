from django.db import models

class Profile(models.Model):
    text = models.CharField(max_length=4096)

class Member(models.Model):
    username = models.CharField(max_length=16,primary_key=True)
    password = models.CharField(max_length=16)
    email = models.CharField(max_length=16, null=True)
    date = models.DateTimeField('date created', null=True)
    about = models.CharField(max_length=500, null=True)
    gender = models.CharField(max_length=16, null=True)
    city = models.CharField(max_length=16, null=True)
    profile = models.OneToOneField(Profile, null=True)
    following = models.ManyToManyField("self", symmetrical=False)
    friends= models.ManyToManyField("self", symmetrical=True)
    def __str__(self):
        return self.username
    def flw(self):
        return self.following

class Requests(models.Model):
      requestFrom = models.CharField(max_length=16, null=True)
      requestTo = models.CharField(max_length=16, null=True)
      def __str__(self):
        return self.requestFrom + " " + self.requestTo

    
class Message(models.Model):
    user = models.ForeignKey(Member, related_name='%(class)s_user')
    recip = models.ForeignKey(Member, related_name='%(class)s_recip')
    pm = models.BooleanField(default=True)
    time = models.DateTimeField()
    text = models.CharField(max_length=4096)
