from django.shortcuts import render,HttpResponse
from index.models import *
import random
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

# Create your views here.

#添加数据
# def index_views(request):
#     for x in range(200):
#         good = Goods(name="good%s"%x,des="该商品物美价廉，现在只需要{}元".format(random.randint(10,100)))
#         good.save()
#
#     return HttpResponse("数据添加成功")

#通过Django中的Paginator来实现代码的实现
def select(request):
    # 查询数据库中的所有数据
    good_list =Goods.objects.all()
    # 值1：所有的数据
    # 值2：每一页的数据
    # 值3：当最后一页数据少于n条，将数据并入上一页
    paginator = Paginator(good_list,12,3)
    try:
        # GET请求方式，get()获取指定Key值所对应的value值
        # 获取index的值，如果没有，则设置使用默认值1
        num =request.GET.get('index','1')
        #获取第几页
        number = paginator.page(num)
    except PageNotAnInteger:
        #如果输入的页码不是整数，那么显示第一页的数据
        number = paginator.page(1)
    except EmptyPage:
        #如果显示的页面为空值是
        number = paginator.page(paginator.num_pages)
    return render(request,'index.html',{'page':number,'paginator':paginator})






