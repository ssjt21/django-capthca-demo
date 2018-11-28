# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.contrib import auth

from django.contrib.auth.decorators import login_required
# Create your views here.



#获取验证码图片
def get_valid_img(request):
    from PIL import  Image,ImageDraw,ImageFont
    import random,string

    #获取随机颜色
    def get_random_color():
        return tuple(map( lambda x:random.randint(0,255),range(3)))

    print get_random_color()
    #生成图片对象

    img_obj = Image.new('RGB',(220,35),get_random_color())

    # 写入文字 画笔对象
    draw_obj = ImageDraw.Draw(img_obj)

    # 使用字体，获取一个字体对象
    font_obj= ImageFont.truetype("static/cour.ttf",28)

    #生成随机字符
    code_str=random.sample(string.letters,5)
    for i,ch in enumerate(code_str) :
        draw_obj.text((20+40*i,0),ch,fill=get_random_color(),font=font_obj)

    #验证码的值保存到session中

    request.session['valid_code'] ="".join(code_str)

    #加入干扰线
    width=220
    height=35
    for i in range(5):
        x1,x2=map(lambda x:random.randint(0,width),range(2))
        y1,y2=map(lambda x:random.randint(0,height),range(2))
        draw_obj.line((x1,y1,x2,y2),fill=get_random_color())

    #加入干扰点

    for i in range(40):
        x,y=random.randint(0,width),random.randint(0,height)
        draw_obj.point((x,y),fill=get_random_color())
        x, y = random.randint(0, width), random.randint(0, height)
        draw_obj.arc((x,y,x+4,y+4),0,90,fill=get_random_color())
    #生成的图片不需要保存到磁盘，保存到内存中即可

    from io import  BytesIO
    io_obj=BytesIO()
    img_obj.save(io_obj,'png')
    data=io_obj.getvalue()
    return  HttpResponse(data)



def login(request):

    if request.method == "POST":
        ret={"status":0,"msg":""}
        #获取用户名和密码
        username=request.POST.get("username",None)
        pwd=request.POST.get("password",None)
        valid_code=request.POST.get("valid_code",None)
        print valid_code
        # print request.
        if valid_code and valid_code.upper() ==request.session.get("valid_code","").upper():
            #使用auth模块验证用户名和密码
            user=auth.authenticate(username=username,password=pwd)
            if user:
                #认证成功的话就开始将用户信息写入sesssion
                auth.login(request,user)
                ret["msg"]="/app02/index/"

            else:
                ret['status']=1
                ret['msg']="用户名活密码不正确!"
        else:
            ret['status'] = 1
            ret['msg'] = "验证码错误!"
        #为了安全问题，必须将验证码强制失效
        request.session.flush()
        return JsonResponse(ret)
    return  render(request,'login2.html')

@login_required
def index(request):

    return render(request,'index2.html',{'user':request.user})


def logout(request):
    auth.logout(request)
    return render(request,'login2.html')