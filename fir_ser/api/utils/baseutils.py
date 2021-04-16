#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project: 4月 
# author: NinEveN
# date: 2021/4/16

import os, re
from fir_ser.settings import SUPER_SIGN_ROOT
from api.models import AppReleaseInfo
from api.utils.app.randomstrings import make_app_uuid
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)


def get_app_d_count_by_app_id(app_id):
    d_count = 1
    binary_size = AppReleaseInfo.objects.filter(is_master=True, app_id__app_id=app_id).values('binary_size')
    if binary_size and binary_size > 0:
        d_count += binary_size // 1024 // 1024 // 100
    return d_count


def file_format_path(user_obj, auth=None, email=None):
    if email:
        cert_dir_name = make_app_uuid(user_obj, email)
    else:
        pkey = auth.get("username")
        if auth.get("issuer_id"):
            pkey = auth.get("issuer_id")
        cert_dir_name = make_app_uuid(user_obj, pkey)
    cert_dir_path = os.path.join(SUPER_SIGN_ROOT, cert_dir_name)
    if not os.path.isdir(cert_dir_path):
        os.makedirs(cert_dir_path)
    file_format_path_name = os.path.join(cert_dir_path, cert_dir_name)
    return file_format_path_name


def get_profile_full_path(developer_obj, app_obj):
    pkey = developer_obj.email
    if developer_obj.issuer_id:
        pkey = developer_obj.issuer_id
    cert_dir_name = make_app_uuid(developer_obj.user_id, pkey)
    cert_dir_path = os.path.join(SUPER_SIGN_ROOT, cert_dir_name, "profile")
    provision_name = os.path.join(cert_dir_path, app_obj.app_id)
    return provision_name + '.mobileprovision'


def delete_app_profile_file(developer_obj, app_obj):
    file = get_profile_full_path(developer_obj, app_obj)
    try:
        if os.path.isfile(file):
            os.remove(file)
    except Exception as e:
        logger.error("delete_app_profile_file developer_obj:%s  app_obj:%s file:%s Exception:%s" % (
            developer_obj, app_obj, file, e))


def is_valid_domain(value):
    pattern = re.compile(
        r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
        r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
    )
    return True if pattern.match(value) else False


def is_valid_phone(value):
    phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
    return True if str(value) and re.search(phone_pat, str(value)) else False


def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
