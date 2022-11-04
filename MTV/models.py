from email.mime import image
from tkinter import image_types
from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import os

class Board(models.Model) :
    title = models.CharField(max_length=100)
    content = models.TextField()
    sound = models.FileField(blank= True, null = True, upload_to = 'blog_sound') 
    photo = models.ImageField(blank= True, null = True, upload_to = 'blog_photo') 
    author= models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add = True)
    modify_date = models.DateTimeField(auto_now= True, null=True, blank=True)
    
    def __str__(self) :
            return f'[PK:{self.pk}]-{self.title} :: {self.author}'


    def get_FileName(self) :
        return os.path.basename(self.sound.name)

    def get_ImageName(self) :
        return os.path.basename(self.photo.name)

    def get_absolute_url(self) :
        return f'/MTV/{self.pk}'




class Comment(models.Model):
    document = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)

    def __str__(self):
        return (self.author.username if self.author else "무명")+ "의 댓글"
        