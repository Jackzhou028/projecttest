from random import Random
from userinfo.models import EmailVerifyRecord   # 邮箱验证model
from django.core.mail import send_mail  # 发送邮件模块


def generate_random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars)-1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()   #实例化
    random_str = generate_random_str(8)   #取随机数
    email_record.code = random_str
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    if send_type == "register":
        email_title = "注册激活链接"
        email_body = "请点击下面的链接激活你的账号：http://127.0.0.1:8000/user/active/{0}".format(random_str)
        send_status = send_mail(email_title,email_body,email,[email])
        if send_status:
            pass
