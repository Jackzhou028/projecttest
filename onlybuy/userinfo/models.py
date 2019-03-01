from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
# Create your models here.

SEX_CHOICES = (
    ('1', '男'),
    ('0', '女'),
)


class UserInfo(AbstractUser):
    headp = models.ImageField('头像', upload_to='headphoto', default='/headphoto/touxiang.png', null=False, blank=True)
    nickname = models.CharField('昵称', max_length=30, null=True, blank=True)
    mobile = models.CharField("手机号", max_length=13, null=False)
    email = models.EmailField("邮箱", null=True)
    sex = models.CharField('性别', max_length=10, null=True, blank=True, choices=SEX_CHOICES, default='1')


    def __str__(self):
        return self.username


class Address(models.Model):
    consignee = models.CharField("收件人", max_length=20, null=False, default="any")
    ads = models.TextField("收货地址",null=False)
    mobile = models.CharField("手机号", max_length=13, null=False)
    defaultads = models.BooleanField("是否为默认地址", default=False)
    zipcode = models.CharField("邮编", max_length=30, default="000000")
    alias = models.CharField("别名", max_length=50)
    user = models.ForeignKey(UserInfo)

    def __str__(self):
        return self.user.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50,verbose_name='邮箱')
    send_type = models.CharField(verbose_name='验证码类型',choices=(('register','注册'),('forget','忘记密码')),
                max_length=20)
    send_time = models.DateTimeField(verbose_name='发送时间', default=datetime.datetime.now)

    class Meta:
        verbose_name='邮箱验证码'
        verbose_name_plural=verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code,self.email)