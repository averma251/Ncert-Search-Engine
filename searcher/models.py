from django.db import models

# Create your models here.
class qas(models.Model):
    question = models.TextField()
    a1 = models.TextField()
    a2 = models.TextField()
    a3 = models.TextField()
    a4 = models.TextField()
    a5 = models.TextField()
    cx1 = models.TextField()
    cx2 = models.TextField()
    cx3 = models.TextField()
    cx4 = models.TextField()
    cx5 = models.TextField()
    t1 = models.TextField()
    t2 = models.TextField()
    t3 = models.TextField()
    t4 = models.TextField()
    t5 = models.TextField()

    def __str__(self):
        return self.question

class hist(models.Model):
    cur_time = models.DateTimeField(auto_now_add=True)
    cur_user = models.TextField()
    cur_question = models.TextField()
    
    def __str__(self):
        return self.cur_user
