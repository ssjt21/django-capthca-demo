# -*- coding: utf-8 -*-

"""
@author:随时静听
@file: urls.py
@time: 2018/11/27

"""

from django.conf.urls import  url

from app02 import views

app_name='app02'

urlpatterns=[

    url('^login/',views.login,name='login'),
    url('^get_valid_img.png/',views.get_valid_img,name='get_valid_img'),
    url('^index/',views.index,name="index"),
    url('^logout/',views.logout,name="logout"),
]

if __name__ == '__main__':
    pass
