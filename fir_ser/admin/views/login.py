#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project: 4月
# author: liuyu
# date: 2021/4/11

import logging

from django.contrib import auth
from rest_framework.views import APIView

from api.models import UserInfo
from api.utils.auth.util import AuthInfo
from api.utils.serializer import UserInfoSerializer
from api.utils.utils import set_user_token
from common.core.auth import ExpiringTokenAuthentication
from common.core.response import ApiResponse
from common.core.sysconfig import Config
from common.core.throttle import VisitRegister1Throttle, VisitRegister2Throttle
from common.utils.caches import login_auth_failed

logger = logging.getLogger(__name__)


class LoginView(APIView):
    throttle_classes = [VisitRegister1Throttle, VisitRegister2Throttle]

    def post(self, request):
        receive = request.data
        username = receive.get("username", None)
        code = 1000
        msg = 'success'
        data = None
        # if Config.LOGIN.get("captcha"):
        #     is_valid = valid_captcha(receive.get("captcha_key", None), receive.get("verify_code", None), username)
        # else:
        #     is_valid = True
        if True:
            if login_auth_failed("get", username):
                password = receive.get("password")
                user = auth.authenticate(username=username, password=password)
                logger.info(f"username:{username}  password:{password}")
                if user:
                    if user.is_active:
                        # if user.role == 3:
                            login_auth_failed("del", username)
                            key, user_info = set_user_token(user, request)
                            data = {
                                "username": user_info.username,
                                "token": key
                            }
                        # else:
                        #     msg = "权限拒绝"
                        #     code = 1003
                    else:
                        msg = "用户被禁用"
                        code = 1005
                else:
                    login_auth_failed("set", username)
                    msg = "密码或者账户有误"
                    code = 1002
            else:
                code = 1006
                logger.error(f"username:{username} failed too try , locked")
                msg = "用户登录失败次数过多，已被锁定，请1小时之后再次尝试"
        else:
            code = 1001
            msg = "验证码有误"

        return ApiResponse(code=code, msg=msg, data=data)

    def get(self, request):
        auth_obj = AuthInfo(Config.LOGIN.get("captcha"), False)
        data = auth_obj.make_rules_info()
        return ApiResponse(data=data)


class LoginUserView(APIView):
    throttle_classes = [VisitRegister1Throttle, VisitRegister2Throttle]
    authentication_classes = [ExpiringTokenAuthentication, ]

    def get(self, request):
        serializer = UserInfoSerializer(request.user, )
        return ApiResponse(data=serializer.data)

    def post(self, request):
        data = request.data
        user_id = data.get('user_id')
        password = data.get('password')
        if user_id and password and len(password) >= 6:
            user_obj = UserInfo.objects.filter(pk=user_id).first()
            if user_obj:
                user_obj.set_password(password)
                user_obj.save(update_fields=['password'])
            serializer = UserInfoSerializer(user_obj, )
            return ApiResponse(data=serializer.data)
        return ApiResponse(code=1001, msg='重置密码失败，用户不存在')
