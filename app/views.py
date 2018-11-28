# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse,redirect

# Create your views here.


#滑动验证码导入

from geetest import GeetestLib

from django.http import  JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
#请在官网申请ID使用，示例ID不可使用
pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"




def getcaptcha(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


def login(request):
    if request.method == "POST":
        ret={"status":0,"msg":""}
        #获取用户名和密码
        username=request.POST.get("username",None)
        pwd=request.POST.get("password",None)
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            #使用auth模块验证用户名和密码
            result = gt.success_validate(challenge, validate, seccode, user_id)

        else:
            result = gt.failback_validate(challenge, validate, seccode)

        if result:
            user = auth.authenticate(username=username, password=pwd)
            if user:
                # 认证成功的话就开始将用户信息写入sesssion
                auth.login(request, user)
                return redirect('/app/index/')

            else:
                ret['status'] = 1
                ret['msg'] = "用户名活密码不正确!"
        else:
            ret['status'] = 1
            ret['msg'] = "验证码错误!"
        return render(request, 'login.html',{'ret':ret})
    return  render(request,'login.html')

@login_required(login_url='/app/login/')
def index(request):
    return  render(request,'index2.html',{'user':request.user})