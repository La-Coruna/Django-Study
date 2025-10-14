from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE, # 계정 삭제하면 작성한 글들 다 사라짐
        related_name='author_question'
    )
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(
        to=User,
        related_name='voter_question'
    )
    
    def __str__(self):
        return self.subject


class Answer(models.Model):
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='author_answer'
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(
        to=User,
        related_name='voter_answer'
    )
    
class Comment(models.Model):
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='author_comment'
    )
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(
        to=Question,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    answer = models.ForeignKey(
        to=Answer,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )