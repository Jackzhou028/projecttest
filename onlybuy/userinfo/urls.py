from django.conf.urls import url
from .views import *
from . import viewsUtil
urlpatterns = [
    # url('^/', , name=''),
    url('login', login_, name='login'),
    url('register', register_, name='register'),
    url('logout', logout_, name='logout'),
    url('checkusername', checkusername, name='checkusername'),
    url('addads', add_ads, name='addads'),
    url('adslst', adslst, name='adslst'),
    url('defads', default_ads, name='defads'),
    url('delads', del_ads, name='delads'),
    url('verifycode', viewsUtil.verifycode),
    url('verifycodeValid', verifycodeValid),
    url('active', activemail),
    url('alterinfo', alter_info, name='alterinfo'),
    url('changepwd', change_pwd, name='changepwd'),
]
