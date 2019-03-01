from django.http import HttpResponse
import re

def reusername(username):
    username_pat = re.compile('^.{6, 9}$')
    res = re.search(username_pat, username)
    if res:
        return HttpResponse("ok")
    else:
        return HttpResponse("no")


def repassword(password):
    password_pat = re.compile('^[A-Za-z][A-Za-z1-9_-]{5, 8}$')
    res = re.search(password_pat, password)
    if res:
        return HttpResponse("ok")
    else:
        return HttpResponse("no")



def remoile(mobile):
    mobile_pat = re.compile('^(13\d|15\d|17[3|6|7]|18\d)\d{8}$')
    res = re.search(mobile_pat, mobile)
    if res:
        return HttpResponse("ok")
    else:
        return HttpResponse("no")


def reemail(email):
    email_pat = re.compile('^(\w)+(.\w+)*@(\w)+((.\w+)+)$')
    res = re.search(email_pat, email)
    if res:
        return HttpResponse("ok")
    else:
        return HttpResponse("no")