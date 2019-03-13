from django.db import models

# Create your models here.

class Goods(models.Model):
    name = models.CharField("姓名",max_length=100)
    des = models.CharField("详细描述",max_length=1000)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "goods"
        verbose_name = "商品表"
        verbose_name_plural = verbose_name


