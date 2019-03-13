from django.db import models

# Create your models here.

class UserList(models.Model):
    username = models.CharField(max_length=32)
    age = models.IntegerField()

    def __str__(self):
        return self.username

    class Meta:
        db_table = "userlist"
        verbose_name = "用户信息表"
        verbose_name_plural = verbose_name