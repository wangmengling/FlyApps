#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project: 7月 
# author: NinEveN
# date: 2021/7/19
import os

API_DOMAIN = "https://app.hehelucky.cn"
WEB_DOMAIN = "https://app.hehelucky.cn"
MOBILEPROVISION = "https://ali-static.jappstore.com/embedded5.mobileprovision"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class BASECONF(object):
    VERSION = '1.3.1'

    DEBUG = True

    SECRET_KEY = 'j!g@^bc(z(a3*i&kp$_@bgb)bug&^#3=amch!3lz&1x&s6ss6t'

    ALLOWED_HOSTS = ['127.0.0.1', 'synchrotron', '172.16.133.34', 'ali.cdn.flyapp.dvcloud.xin',
                     'api.src.flyapp.dvcloud.xin', 'app.hehelucky.cn']

    # When Django start it will bind this host and port
    # ./manage.py runserver 127.0.0.1:8080
    # uwsgi运行时绑定端口
    SERVER_BIND_HOST = '127.0.0.1'
    SERVER_LISTEN_PORT = 8898

    # celery flower 任务监控配置
    CELERY_FLOWER_PORT = 5566
    CELERY_FLOWER_HOST = '127.0.0.1'

    # geetest 配置信息
    GEETEST_ID = "d3f3cf73200a70bd3a0c32ea22e5003a"
    GEETEST_KEY = "6f4ab6185c230a4b1f8430f28ebe4804"
    GEETEST_CYCLE_TIME = 10
    GEETEST_BYPASS_STATUS_KEY = "gt_server_bypass_status"
    GEETEST_BYPASS_URL = "http://bypass.geetest.com/v1/bypass_status.php"

    # 访问速率限制
    DEFAULT_THROTTLE_RATES = {
        'ShortAccessUser1': '180/m',
        'ShortAccessUser2': '2000/h',
        'LoginUser': '200/m',
        'RegisterUser1': '40/m',
        'RegisterUser2': '300/h',
        'GetAuthC1': '60/m',
        'GetAuthC2': '300/h',
        'InstallAccess1': '10/m',
        'InstallAccess2': '20/h',
        'ReceiveUdid1': '20/h',
        'ReceiveUdid2': '30/h',
    }


class DBCONF(object):
    host = '127.0.0.1'
    port = '3306'
    password = 'KGzKjZpWBp4R4RSa'
    user = 'flyuser'
    name = 'flyapp'


class CACHECONF(object):
    host = '127.0.0.1'
    port = '6379'
    password = ''


class STORAGEKEYCONF(object):
    STORAGE = [
        {
            'name': 'local',
            'type': 0,
            'auth': {
                'domain_name': API_DOMAIN.split("://")[1],
                # 正式环境需要填写正式的访问域名,如果配置cdn，可以填写cdn的域名，仅支持阿里云 cdn,
                # 开启cdn之后，如果该域名和服务器域名不相同，需要设置阿里云cdn 缓存配置，自定义HTTP响应头 添加 Access-Control-Allow-Origin * 才可以
                'is_https': True if API_DOMAIN.split("://")[0] == "https" else False,
                'download_auth_type': 1,  # 0:不开启token 1:本地token 2:cdn 开启cdn，并且使用本地存储，使用阿里云cdn进行url鉴权，
                'cnd_auth_key': '',  # 当cdn为阿里云并且 download_auth_type=2 的时候 生效,需要 开启阿里云OSS私有Bucket回源
            },
            'active': True
        },
        {
            'name': 'aliyun',
            'type': 2,
            'auth': {
                'access_key': 'LTAI4FkbTR',
                'secret_key': '2iLIxy9',
                'bucket_name': 'fge',
                'sts_role_arn': 'ap-sage',
                'endpoint': 'oss-cn-beijing-internal.aliyuncs.com',  # 服务器和oss在同一个地区，填写内网的endpoint
                'is_https': True,
                'domain_name': 'aoud.xin',
                'download_auth_type': 1,  # 1:oss 2:cdn
                'cnd_auth_key': '',  # 当cdn为阿里云并且 download_auth_type=2 的时候 生效,需要 开启阿里云OSS私有Bucket回源
            },
            'active': False
        },
        {
            'name': 'qiniuyun',
            'type': 1,
            'auth': {
                'access_key': 'mT4fiJ',
                'secret_key': '0G9fXfhYLynv',
                'bucket_name': 'fge',
                'is_https': False,
                'domain_name': 'foud.xin'
            },
            'active': False
        }
    ]


class SENDERCONF(object):
    SENDER = [
        {
            'name': 'email',
            'type': 0,
            'auth': {
                'email_host': 'smtp.126.com',
                'email_port': 465,
                'use_tls': False,
                'use_ssl': True,
                'username': 'flyapps@126.com',
                'password': 'GGHFEUMZBRZIFZGQ',
                'form': 'fly分发平台 <flyapps@126.com>',
                'subject': '%(code)s验证',
                'template_code': {
                    'login': '欢迎使用FLY 应用分发平台。 您的验证码%(code)s ，您正在登录，若非本人操作，请勿泄露。',
                    'change': '欢迎使用FLY 应用分发平台。 您的验证码%(code)s ，您正在尝试变更重要信息，请妥善保管账户信息。',
                    'register': '欢迎使用FLY 应用分发平台。 您的验证码%(code)s ，您正在注册成为新用户，感谢您的支持！',
                    'password': '欢迎使用FLY 应用分发平台。 您的新密码为%(code)s ， 请用新密码登录之后，及时修改密码，并妥善保管账户信息。',
                    'common': '欢迎使用FLY 应用分发平台。 您的验证码%(code)s ， 若非本人操作，请忽略。'
                }
            },
            'active': True
        },
        {
            'name': 'aliyun',
            'type': 1,
            'auth': {
                'access_key': 'LTAI5tJH2EnjVzJGMmNCYo9U',
                'secret_key': 'd0LETks5oxkdfbkLGtFihklWGbokab',
                'region_id': 'cn-hangzhou',
                'sing_name': '东城飞阳',
                'template_code': {
                    'login': 'SMS_216700569',
                    'change': 'SMS_216700566',
                    'register': 'SMS_216700567',
                    'password': 'SMS_222341718',
                    'common': 'SMS_227259072'
                }
            },
            'active': True
        },
        {
            'name': 'jiguang',
            'type': 2,
            'auth': {
                'app_key': '93e1a9f71db4f044de4db34a',
                'master_secret': '5f996ee39c7eb52906510cc2',
                'sign_id': '18138',
                'template_code': {
                    'login': '1',
                    'change': '1',
                    'register': '1',
                    'password': '1',
                    'common': '1',
                }
            },
            'active': False
        },
    ]


class PAYCONF(object):
    PAY_SUCCESS_URL = '%s/user/orders' % WEB_DOMAIN  # 前端页面，支付成功跳转页面
    PAY_CONFIG_KEY_INFO = [
        {
            'NAME': 'alipay',
            'TYPE': 'ALI',
            'ENABLED': True,
            'AUTH': {
                'APP_ID': "2021002138691845",
                'APP_PRIVATE_KEY': '''-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAhqf2mwftoxZDNpl4eWsQ6mEfXgMlNPr6jv72ecA4hbKWqChXQmGS1T+0VsRTSoOXRDlu1MMqkTGISzHvmGb7Gmw+Myfs/ojoonD9r8fODvIo1MHolFBhr3GNQu7tqBlVJ76QgiYft+c4kkqCguuyCrd3Te6C5zCIuh6O98r4D3A3LFcm6OdScWGcfEbR+FUv+jSi2oezHeSpkhhpHGBLSsI0L9JOdHetdUE/TwN8V1HABdpnPXtp9SIu6ioIrrligX1ZRlwht2YUt0BPqPp/ApLdRIsqlhD4/ejmtMlaRqqiN6PulEThBew/qaLVSXIr2HCSXtwbki3pFMFOcsjF2wIDAQABAoIBADp4sQL83FnXDvSki8XdkgjUh7RhFUT+PtLdL9YKfADCXd1DNzDiAcqL0RlkQu62WXcMoW3OGavWoGJWmr3I6fy9R/0atzSH6syu19n+nyGqUcShNwdAKErwufB4o8Y8yddqToHVYCyRQOV1aVrEUhmJNUsn6LvPPW/kWRyMjE7XQDFHpL5/Ly7pXe+f9Btm37ZuePTPsm65P88C3GznjZxXhY1LBWFKLPG1470xdReduyeJFZS/TmK0nUxLwkACm9Gfvp7S2KJ3okUXohsGBAgJ68B9YeGiuIJiZhH2DZ1pm3/R9bSpOX3H+6vjaCsacXT5w7LZB+O0Vkthcm9vqeECgYEAvozFkIkFXXCEmCr3QVCJs4Fc6onbXEJU45xxubPhkA1wwwPrSqdubo4RHvNIus45Fn4mLzuQsaPRyJJZajvaKWC00GxhChMYj+nWgkAmABPKGwkMxzjC7wvEJkGyt87fHpK1XMFWQgfJ42VwUtmyemCMuh+A2SOekIJay93xTtkCgYEAtOhmQ4pu2cyqTzT+SD7p/VnS4sNqqM4I8NSvTuLkEo2IHnUj7YG6XoPZjn35dBvYUWWN2dwgfHXGEEzCOIwfy8GPA4eoKCDNEkMvoBVLdrEzMqg5QwG5GsIGvOuFnAzAw+D5YwEym/qmC2oBbat5jsAGT2rMmU5MnaS8a7lvcdMCgYEAiusQQb5TZfrZACMa3cg8i9y9A9R7UzicsM/mbW+B+8aAtfxOdr+4F+uE+d594IrmPcq8ReUUKR34nFRt0bBO7amuSOEqofCoEIt3MsBXs+i5iJpBcaClJSeb2hQ9mhm8uopUpInjPAJ3okva5twFbYikMDE1e5inSk1uqoBlI4kCgYB4rzDJjeg1U9upy2h3OcFPSkTtEgBtbEV6o+fvcF1GIzTTXMIDB7AUrVDNRizL0GeWpXDkDX1+ifL/nLVUk+YCP7XwXOdJHdiwfjGfUZVuMPg+qwrIMLYTq6xjC5uuZrOR+NtluL7SX3u10ZnyV5pYKLIM+OpUu29RGzy3gJVgEQKBgCC9vXS7P9RHTAxYEG4WOzv0tjFUtPOsaHenvNbc7nVe2Kkre0/TO+EtnuhINmJp2y5UEve6cLK2sPnbT8raarjPuomDfN0hwEx3jZd+rPdB/tdRH0LMLBu28TlzHllJYjbINn+NXc0adbqeuA4ziXTZow5yX5J+i9dy55A1bvie
-----END RSA PRIVATE KEY-----''',
                'ALI_PUBLIC_KEY': '''-----BEGIN CERTIFICATE-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkru1ulQV1v4q+q38nyzgkdd3evf7C1/Ipu6K+ZFb5FiuxJ7mildkBSuKz/8+TRd+tjgk2lfc2ehK5pja3cxDO/nb25sBoWiU09rtxgXLehLsgRRhatbICrlOnYxg5aiB5odAp3NMRqore4lnVYwfIyL9M49I0G/NbQzYjUQvAQJsnHwc6a6Kuqi1CwR1WXI0sDF9w7KXC4vRFFIUTwI4bVq4HQWI7NhbgEajHM/j6D6Bh/OMcTYnJJzCja0WmZRe5flfCsELlPESOCWUMbYoaNfBzpNvvyOpmRgs9jgy2WY9SeaB9hxwkpr8tOd2Sc7j3221JKCyDaFAX+4zPy7/fQIDAQAB
-----END CERTIFICATE-----''',
                'APP_NOTIFY_URL': '%s/api/v1/fir/server/pay_success' % API_DOMAIN,  # 支付支付回调URL
                'RETURN_URL': PAY_SUCCESS_URL,  # 支付前端页面回调URL
                'SUBJECT': '向 FLY分发平台 充值',
            }
        },
        {
            'TYPE': 'WX',
            'NAME': 'wxpay',
            'ENABLED': True,
            'AUTH': {
                'APP_ID': "wx390e5985fd3699e6",
                'MCH_ID': "1608486112",
                'SERIAL_NO': "27DADA4D2921CDD66B8B20A68276F09B90754922",
                'APP_PRIVATE_KEY': '''-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDbXhNoHljrkS8T
jXg3+tTkaoOol8FDt0jSGckhzX46gkS16CWYwTthBKurfFtynsJe4uDOphS1ge/r
QEU3+rWNxqa8o6gHSpp2UTYAz/1oYOlXuSa4NA1uD47lmVZJzad2ybWDSsoeRjFj
c+X6F0ZiE3FmdN1iHz8NmbP99foih4smv15X+wX5DrsuLuPVHNB4D0fqvY7P5PO3
wUQXWQNezCYzpPoXX2H/UkyFEFZhWk6/9z3aAkYmqfd6IWPHewOqnVoQRKmo5bXb
yWbB+QIl/HcSfNtq869s5lLGR2Rl2UX8IFXCcXnRPhSAVIeWfXN26Pc9dz9N4VTU
yiZ8Y6AHAgMBAAECggEABdS0U1orJufPBogGIAbMzd1+7mZKPtCKYPtKe1mI92kr
BmLLTQol1+hV39MIYz2RERCaxSNo/YIcrHYi4OALH1+eYvk+qCL1hBuYgeEFbVbW
HPzQ6KiJitljBPtUbdXHk8K8zmaYhMF84pXcEQ+5UTYPF5gXoloORQBG5oM5SN2g
2GTgYw1cpDzzRRwnmpvYd1ZydYNj8m6k7I2L1pwzRS/6/whz1sScpfh+91w1IVM0
WT+pPSdiVtQ7ktmvcTrWj7eNIbcsptZ1QgSV3UHkU0xzLG9N1TqJdHOquunXRS7V
iw/4NgXveXSTSQrmmZVS+Kdyc+z1iDqwOXmE7hjioQKBgQD7js+40NCAPLYXEfer
UFvZ6kem9mJIzAUdeTdK4BjYJrcU+UsXRmcWJIPI9HWSr31f/fSfu2SKyBa6+dFF
SeNHuHPPqQAXrsNuhFG1wcKoNybk7KrsQlXheK7br42565Tegz3UXOKMrnPPlukH
ZZdlYmwBFjEJvIr9jxJvJoW6qQKBgQDfPb697vR8ruLaecPmsq920iC3AQRanYFK
dW6U98JkCN9A/LXA1jGyDTEhtlja+5Ylp0M1EnlcZ079Jnvek5haSNnD0xb1nMy8
P/o0/eWWArTgfjfiJeq1tSdrinGhNz0+Vty74wnbS+5P18H23I5jBlGX5hyNkU4L
axUfJM9jLwKBgCo/1xVkRNB04eRICT/FlFeqKHSbRvCRC37iv+2ca6/J+M/V+s2i
7mdipJuYqzKCtNztayt0rrM8Xczzbjlj6n8+NH05FiHkIUCriomrTEUyVh72vNJH
ZeMjgMK23mfOcEda5YSIQSh9mEfSQbsTTfUiLZ+VGZFYEEP7xo3Se31ZAoGBAJas
LPYytq8EtrYwowktJwJydoQt2otybRYdRmKjCn/MASrypZWeu/Hpt3SCh1xdnAyT
5OeILYMxcv2noMksIxMkwl3KNl/V0dVo9O4ZQ4DJGN3AMuWfI9g6iX2q9mCSUPKn
W9owNbHegN1AyXhdinjJhf6Y4EKohN1uC9Z2WMcfAoGAW90Z2LkqG2fen+R62syP
aaInnu9bitb9rVENCNGXQHdWmIYBMM5zrg8nX8xNJ+yeGQhgxE+YeSq4FOpe0JkA
daWIhg++OHN2MBRutj7oL/AFAxyu467YA5+itEJLHNATbOr/s13S66nePNXox/hr
bIX1aWjPxirQX9mzaL3oEQI=
-----END PRIVATE KEY-----''',
                'API_V3_KEY': '60DbP621a9C3162dDd4AB9c2O15a005L',
                'APP_NOTIFY_URL': '%s/api/v1/fir/server/pay_success' % API_DOMAIN,  # 支付支付回调URL
                'RETURN_URL': PAY_SUCCESS_URL,  # 支付前端页面回调URL
                'SUBJECT': '向 FLY分发平台 充值',
            }
        }
    ]
