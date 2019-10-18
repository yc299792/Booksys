from django.shortcuts import render,redirect #重定向函数和下面的一样
from Book.models import *
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from datetime import date
from django.views.decorators.csrf import csrf_exempt
# 配置项
from django.conf import settings



# Create your views here.
#定义一个登录装饰器装饰只有在用户登录后才能访问的页面
def login_check(view_fun):
    def wrap(request,*args,**kwargs):
        if request.session.has_key('login'):
            return view_fun(request,*args,**kwargs)
        else:
            return redirect('/login')
    return wrap

def index(request):
    print(request.META['REMOTE_ADDR'])
    return render(request,'Book/index.html')

def booklist(request):

    booklist = BookInfo.objects.all()
    # for foo in booklist:
    #     print(foo.name)
    return render(request,'Book/booklist.html',{'booklist':booklist,})

def create(request):

    book = BookInfo()
    book.name = '西游记'
    book.pub_date = date(1990,1,1)
    book.save()
    # 返回一个地址对象，让浏览器去访问新的地址，重定向的,加了/代表直接在域名后加，否则如果之前的域名末尾有/则会拼接上去
    return HttpResponseRedirect('/booklist')

def delete(request,bid):
    book = BookInfo.objects.get(id=bid)
    # book.isDelete = True
    book.delete()

    # return HttpResponseRedirect('/booklist')
    return redirect('/booklist')

def setsession(request):

    if request.session.has_key('password'):
        return HttpResponse('已设置session')
    else:
        request.session['password'] = '1234'
        return HttpResponse('设置session')

def getsession(request):
    if request.session.has_key('password'):
        return HttpResponse(request.session['password'])
    else:
        return HttpResponse('未设置')

def propleinfos(request):
    peolist = PeopleInfo.objects.all()
    return render(request,'Book/peolist.html',{'peolist':peolist})

def child(request):
    return render(request,'Book/child.html')

def htmlescape(request):

    context = '<h1>hello</h1>'
    return render(request,'Book/htmlescape.html',{'context':context})

def csrf(request):
    return render(request,'Book/csrf.html')

def csrfcheck(request):
    return HttpResponse('success')

def login(request):
    """登录页面"""
    return render(request,'Book/login.html')


def logincheck(request):


    if request.POST.get('username') == 'yc' and request.POST.get('password') == '1234' and request.POST.get('vcode') == request.session['verifycode']:
        response = redirect('/change_pwd')
        if not request.session.has_key('login'):
            request.session['login'] = True
        if 'username' not in request.COOKIES:
            response.set_cookie('username',request.POST.get('username'))

        return response
    else:
        # return HttpResponse('用户名密码错误！')

        return redirect('/login')


@login_check
def change_pwd(request):
    return render(request,'Book/changepwd.html')

@login_check
def changepwdcheck(request):
    return HttpResponse('username:'+request.COOKIES['username']+'    newpwd:'+request.POST.get('newpwd'))


from PIL import Image, ImageDraw, ImageFont
from django.utils.six import BytesIO

# 生成验证码
def verifyCode(request):
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
    20, 100), 255)
    width = 100
    height = 35
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('C:\Windows\Fonts\javatext.ttf', 23)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # 内存文件操作
    buf = BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

def fan(request):
    return render(request,'Book/fan.html')

def keyword(request,a,b):
    return HttpResponse(a+':'+b)

def positionword(request,a,b):
    return HttpResponse(a + ':' + b)

# 视图中反向解析
from django.urls import reverse
def redirect_index(request):
    # return redirect(reverse('Book:index'))#首页
    # return redirect(reverse('Book:key',kwargs={'a':1,'b':15}))#关键字参数
    return redirect(reverse('Book:position',args=(20,13)))#位置参数

def upimage(request):
    return render(request,'Book/upimage.html')

def recv(request):

    # pic是一个对象根据文件大小进行划分，2.5m为界限，小于存在内存中，大于存为临时文件
    pic = request.FILES.get('upimage')
    name = pic.name
    path = "%s/BOOK/%s"%(settings.MEDIA_ROOT,name)

    with open(path,'wb') as fw:
        for c in pic.chunks():
            fw.write(c)

#     保存路径到数据库
    picpath = PictureInfo()
    picpath.path = "Book/%s"%name
    picpath.save()

    return HttpResponse('上传成功')


from django.core.paginator import Paginator
def book(request):

     return render(request,'Book/book.html')

def books(request):

    book = BookInfo.objects.all()

    booklist = []

    for foo in book:
        booklist.append((foo.id, foo.name))

    data = {'data': booklist}

    return JsonResponse(data)

def peoples(request):

    b = BookInfo.objects.get(id = request.GET['bookid'])
    peo = PeopleInfo.objects.filter(book = b)

    peolist = []
    for foo in peo:
        peolist.append((foo.id,foo.name))

    return JsonResponse({'data':peolist})

def des(request):

    peo = PeopleInfo.objects.get(id = request.GET['peoid'])

    return JsonResponse({'data':peo.description})
