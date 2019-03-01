from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout, login, authenticate
from django.core import serializers
from .models import *
from .repa import *
import logging
import json
import re
import base64
import random
import datetime


# Create your views here.


def check_login_status(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
        # user = UserInfo.objects.get(username='asdfgh')
        # if user:
        #     request.user = user
            return func(request, *args, **kwargs)
        else:
            return HttpResponse(json.dumps({"result": False, "data": "", "error": "未登录"}))
    return wrapper


# 登录
def login_(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        result = verifycodeValid(request)
        if result == "no":
            return HttpResponse(json.dumps({"result": False, "data":"", "error":"验证码错误"}))
        if username and password:
            # 使用django提供的验证方法，传入用户名和密码，会返回一个user对象
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return HttpResponse(json.dumps({"result": True, "data": username, "error": ""}))
            else:
                return HttpResponse(json.dumps({"result": False, "data": "", "error": "用户名或密码错误"}))
        else:
            return HttpResponse(json.dumps({"result":False, "data":"", "error":"输入项不能为空"}))


# 注册
def register_(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        mobile = request.POST.get('mobile', '')
        email = request.POST.get('email', '')
        if username and password and mobile and email:
            olduser = UserInfo.objects.filter(username=username)
            if olduser:
                return HttpResponse(json.dumps({"result":False, "data":"", "error":"该用户名已经存在"}))
            else:
                password = make_password(password, None, 'pbkdf2_sha1')
                try:
                    UserInfo.objects.create(username=username, nickname=username, password=password, mobile=mobile, email=email)
                except DatabaseError as e:
                    logging.warning(e)
                    return HttpResponse(json.dumps({"result": False, "data": "", "error": ""}))
                return HttpResponse(json.dumps({"result": True, "data": "注册成功", "error": ""}))
        else:
            return HttpResponse(json.dumps({"result":False, "data":"", "error":"输入项不能为空"}))


# 校验用户名
def checkusername(request):
    if request.method == 'GET':
        username = request.GET.get('username', '')
        if username:
            olduser = UserInfo.objects.filter(username=username)
            if olduser:
                return HttpResponse(json.dumps({"result":False, "data":"", "error":"该用户已经存在"}))
            else:
                return HttpResponse(json.dumps({"result":True, "data":"正确", "error":""}))
        else:
            return HttpResponse(json.dumps({"result":False, "data":"", "error":"用户名不能为空"}))


# 注销
@check_login_status
def logout_(request):
    logout(request)
    return HttpResponse(json.dumps({"result":True, "data":"退出成功", "error":""}))


# 添地址
@check_login_status
def add_ads(request):
    if request.method == 'POST':
        user = request.user
        consignee = request.POST.get("consignee")
        ads = request.POST.get("ads")
        mobile = request.POST.get("mobile")
        zipcode = request.POST.get("zipcode")
        alias = request.POST.get("alias")
        if consignee and ads and mobile:
            mobile_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
            res = re.search(mobile_pat, mobile)
            if res:
                adsa = Address.objects.filter(user=user)
                if not adsa:
                    address = Address()
                    address.consignee = consignee
                    address.ads = ads
                    address.mobile = mobile
                    address.defaultads = True
                    address.zipcode = zipcode
                    address.alias = alias
                    address.user = user
                    address.save()
                else:
                    address = Address()
                    address.consignee = consignee
                    address.ads = ads
                    address.mobile = mobile
                    address.zipcode = zipcode
                    address.alias = alias
                    address.user = user
                    address.save()
            else:
                return HttpResponse(json.dumps({"result":False, "data":"", "error":"非手机号"}))
            adss = Address.objects.filter(user=user)
            data = serializers.serialize("json", adss)
            return HttpResponse(json.dumps({"result": True, "data": data, "error": ""}))
        else:
            return HttpResponse(json.dumps({"result":False, "data":"", "error":"输入项不能为空"}))

# 地址列表
@check_login_status
def adslst(request):
    user = request.user
    adss = Address.objects.filter(user=user)
    data = serializers.serialize("json", adss)
    return HttpResponse(json.dumps({"result": True, "data": data, "error": ""}))


# 修改默认地址
@check_login_status
def default_ads(request):
    if request.method == 'POST':
        user = request.user
        adid = request.POST.get("adid")
        try:
            Address.objects.filter(user=user).update(defaultads=False)
            ads = Address.objects.filter(user=user, id=adid)
            if ads:
                ads.update(defaultads=True)
            else:
                return HttpResponse(json.dumps({"result": False, "data": "", "error": "暂无该地址"}))
        except DatabaseError as e:
            logging.warning(e)
            return HttpResponse(json.dumps({"result":False, "data":"", "error":""}))
        return HttpResponse(json.dumps({"result": True, "data": "修改默认地址成功", "error": ""}))


# 删除地址
@check_login_status
def del_ads(request):
    if request.method == 'GET':
        user = request.user
        adid = request.GET.get("adid")
        try:
            delads = Address.objects.get(user=user, id=adid)
            if delads.defaultads is True:
                delads.delete()
                Address.objects.filter(user=user).update(defaultads=True)
            else:
                delads.delete()
            adss = Address.objects.filter(user=user)
            data = serializers.serialize("json", adss)
            return HttpResponse(json.dumps({"result": True, "data": data, "error": ""}))
        except BaseException as e:
            return HttpResponse(json.dumps({"result":False, "data":"", "error":"暂无该地址"}))


# 验证码效验
def verifycodeValid(request):
    if request.method == 'POST':
        vc = request.POST['vc']
        print(vc)
        if vc.upper() == request.session.get('verifycode'):
            return 'ok'
        else:
            return 'no'


# 邮箱通过验证，将用户变为活跃状态
def activemail(request, active_code):
    code_record = EmailVerifyRecord.objects.filter(code=active_code)[0]
    if code_record:
        email = code_record.email
        user = UserInfo.objects.get(email=email)
        # 激活用户
        user.is_active = True
        user.save()
        return HttpResponse("ok")
    else:
        return HttpResponse("no")


# 修改个人信息
@check_login_status
def alter_info(request):
    if request.method == 'POST':
        user = request.user
        headname = user.username
        headp = request.POST.get('headphoto')[22:]
        if headp != '':
            headph = base64.b64decode(headp)
            with open('./images/headphoto/'+headname+'.png','wb') as f:
                f.write(headph)
        headurl = '/headphoto/'+headname+'.png'
        nickname = request.POST.get('nickname')
        sex = request.POST.get('sex')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        rem = remoile(mobile)
        ree = reemail(email)
        if rem == 'no':
            return HttpResponse(json.dumps({"result": False, "data": "", "error": "请输入正确手机号"}))
        if ree == 'no':
            return HttpResponse(json.dumps({"result": False, "data": "", "error": "请输入正确邮箱"}))
        try:
            userinfo = UserInfo.objects.filter(username=user.username)[0]
            userinfo.headp = headurl
            userinfo.nickname = nickname
            userinfo.sex = sex
            userinfo.mobile = mobile
            userinfo.email = email
            userinfo.save()
        except DatabaseError as e:
            logging.warning(e)
            return HttpResponse(json.dumps({"result": False, "data":"", "error": "异常"}))
        data = {}
        data['headp'] = '/images' + str(userinfo.headp)+'?co='+str(random.randint(0,9))+str(random.randint(65, 90))
        data['nickname'] = userinfo.nickname
        data['sex'] = userinfo.sex
        data['mobile'] = userinfo.mobile
        data['email'] = userinfo.email
        return HttpResponse(json.dumps({"result":True, "data":data, "error":""}))
    if request.method == 'GET':
        user = request.user
        userinfo = UserInfo.objects.filter(username=user.username)[0]
        data = {}
        data['headp'] = '/images' + str(userinfo.headp)+'?co='+str(random.randint(0,9))+str(random.randint(65, 90))
        data['nickname'] = userinfo.nickname
        data['sex'] = userinfo.sex
        data['mobile'] = userinfo.mobile
        data['email'] = userinfo.email
        return HttpResponse(json.dumps({"result":True, "data":data, "error":""}))


# 修改密码
@check_login_status
def change_pwd(request):
    if request.method == 'POST':
        user = request.user
        oldpassword = request.POST.get('oldpassword')
        newpassword = request.POST.get('newpassword')
        if oldpassword and newpassword:
            userinfo = authenticate(username=user.username, password=oldpassword)
            if userinfo:
                    password = make_password(newpassword, None, 'pbkdf2_sha1')
                    UserInfo.objects.filter(username=user.username).update(password=password)
                    logout(request)
                    return HttpResponse(json.dumps({"result": True, "data": "修改成功", "error": ""}))
            else:
                return HttpResponse(json.dumps({"result": False, "data": "", "error": "旧密码错误"}))
        else:
            return HttpResponse(json.dumps({"result": False, "data": "", "error": "输入项不能为空"}))



































