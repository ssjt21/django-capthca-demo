# -*- coding: utf-8 -*-

"""
@author:随时静听
@file: urls.py
@time: 2018/11/27
@email:wang_di@topsec.com.cn
"""

from django.conf.urls import  url

from app import  views

app_name='app'

urlpatterns=[
    url('login/$',views.login,name='login'),
    url('getcaptcha/',views.getcaptcha,name='getcaptcha'),#获取滑动验证码
    url('^index/',views.index),
]


if __name__ == '__main__':
    pass