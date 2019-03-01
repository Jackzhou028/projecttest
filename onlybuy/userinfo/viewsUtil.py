import sys
from django.http import HttpResponse
# 引入绘图模块
from PIL import Image, ImageDraw, ImageFont
# 引入随机函数模块
import random


def rndColor():
    """
    生成随机颜色
    :return:
    """


    return (random.randint(0, 255), random.randint(10, 255), random.randint(64, 255))


def verifycode(request):
    # ip = request.remote_addr
    # print(ip)
    #定义变量，用于画面的背景色、宽、高
    bgcolor = '#997679'
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        # 噪点绘制的范围
        xy = (random.randrange(0, width), random.randrange(0, height))
        # 噪点的随机颜色
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        # 绘制出噪点
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    numb_1 = {"1": "壹", "2": "贰", "3": "叁", "4": "肆", "5": "伍", "6": "陆", "7": "柒", "8": "捌", "9": "玖"}
    numb_2 = random.randint(1, 50)
    sign = ["+","-"]
    numb_1_n = random.randrange(1, 10)
    numb_1_s = str(numb_1_n)
    first_s = numb_1[numb_1_s]
    third_s = str(numb_2)
    sign_n = random.randrange(0, 2)
    second_s = sign[sign_n]
    if sign_n == 0:
        last = numb_1_n + numb_2
    else:
        last = numb_2 - numb_1_n
    last_s = str(last)

    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'


    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象 ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('/usr/share/fonts/truetype/fonts-japanese-gothic.ttf', 23)
    #构造字体颜色
    fontcolors = ['yellow','blue','green','red','orange','pink']
    print(random.sample(fontcolors, 1)[0])
    #绘制4个字
    print(first_s)
    draw.text((5, 2),  '?', font=font, fill=random.sample(fontcolors, 1)[0])
    draw.text((20, 2), second_s, font=font, fill=random.sample(fontcolors, 1)[0])
    draw.text((35, 2), first_s, font=font, fill=random.sample(fontcolors, 1)[0])
    draw.text((60, 2), '=', font=font, fill=random.sample(fontcolors, 1)[0])
    draw.text((75, 2), last_s, font=font, fill=random.sample(fontcolors, 1)[0])
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=rndColor())#释放画笔

    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())

    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = third_s
    #内存文件操作
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


