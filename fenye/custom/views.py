from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
from custom.views import *
from custom.models import *
from django.utils.safestring import mark_safe
# Create your views here.


class Pager(object):
    def __init__(self,current_page):
        self.current_page = int(current_page)

    #把方法伪造属性(1)
    @property
    def item_start(self):
        return (self.current_page-1)*10

    # 把方法伪造属性(2)
    @property
    def item_end(self):
        return (self.current_page)*10

    def page_str(self,all_item,base_url):
        #可以通过divmod(1000,10)，他会的到一个元组，第一个值是值，第二个值是余数，我们就通过判断他是否有余数来判断是否是整页，如果有余数在整页基础加1即可！
        # all_page,div = divmod(all_item,10)
        all_page, div = divmod(all_item, 10)
        # print(all_page)
        # print(div)
        #如果余数大于0，则在总页数上增加1
        if div > 0:
            all_page += 1
        pager_list = []
        '''
        比如翻页，总共显示的页数是11页
        如果总页数 <= 11 比如9页：
        　　那么，还有必要让页码动起来吗？就没必要了直接显示总共页数就行了！start就是1，end就是9就行了
        else：
        　　如果当前页小于6：
        　　　　start:1
        　　　　end:11
        　　如果当前页大于6：
        　　　　start：当前页-5
        　　　　end：当前页+6
        　　　　如果当前页+6 >总页数：
        　　　　　　start：总页数-10
        　　　　　　end：总页数
        '''
        #如果没有这么多的页数，就从1开始，以总的页数为结束位置
        if all_page <= 11:
            start = 1
            end = all_page
        else:
            # 默认可以看到的页码11个
            if self.current_page <= 6:
                start = 1
                end = 11 + 1
            else:
                #默认可以看到的页码11个
                start = self.current_page - 5
                end = self.current_page + 6
                #尾页执行的操作
                if self.current_page + 5 > all_page:
                    start = all_page - 10
                    end =all_page + 1
        #不断的修改start和end的值

        #把页面动态起来传入起始位置和结束位置
        for i in range(start,end):
            #判断是否为当前页
            if i == self.current_page:
                temp = '<a style="color:red;font-size:26px;padding: 5px" href="%s?page=%d">%d</a>' % (base_url, i, i)
            else:
                temp = '<a style="padding: 5px" href="%s?page=%d">%d</a>' % (base_url, i, i)
            #把标签拼接然后返回给前端
            pager_list.append(temp)
        #把上一页和下一页加在pager_list最前面和最后面的位置
        if self.current_page > 1:
            pre_page = '<a href="%s?page=%d">上一页</a>' % (base_url, self.current_page - 1)
        else:
            # javascript:void(0) 什么动作都不执行
            pre_page = '<a href="#">上一页</a>'
        #下一页
        if self.current_page >= all_page:
            next_page = '<a href="javascript:void(0);">下一页</a>'
        else:
            next_page = '<a href="%s?page=%d">下一页</a>' % (base_url, self.current_page + 1)

        pager_list.insert(0, pre_page)
        pager_list.append(next_page)

        s = "".join(pager_list)
        print(s)
        return mark_safe(s)


def user_list(request):
    # for i in range(500):
    #     # dic = {"username":"用户名_d%"%i, "age":i}
    #     user = UserList(username="用户名_%d"%i, age=i)
    #     user.save()
    # return HttpResponse("写入数据成功")

    #获取当前页面
    current_page = request.GET.get('page',1)
    page_obj = Pager(current_page)
    #查询出需要展示的10数据出来
    result = UserList.objects.all()[page_obj.item_start:page_obj.item_end]
    # print("11",page_obj.item_start)
    # print("11",page_obj.item_end)
    #数据库中所有的数据的条数
    all_item = UserList.objects.all().count()
    # print("aa",all_item)
    #通过divmod(500,10)，它会得到一个元组，第一个值是值，第二个值是余数，我们就通过判断它是否有余数来判断是否是整页，如果有余数来判断是否是整页，如果有余数在整页的基础上加1即可！
    pager_str =page_obj.page_str(all_item,'/user_list/')

    return render(request, 'user_list.html', {'result': result, 'pager_str': pager_str})


class JsonResonse(object):
    pass


def ajaxfenye(request):
    try:
        content = request.GET.get('content')
    except:
        content = None

    request.session['content'] = content
    infos = UserList.objects.filter(Q(username__icontains=content))
    info_list = []
    for i in range(len(infos)):
        info_list.append({"username":infos[i].username,
                          "age":infos[i].age,
                          })
    return JsonResponse({"records":info_list})





