import random

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
import logging

from celery_tasks.sms.tasks import send_sms_code
from meiduo_mall.libs.captcha.captcha import captcha
from meiduo_mall.utils.yuntongxun.sms import CCP
from .serializers import ImageCodeCheckSerializer

from . import constants

logger = logging.getLogger('django')

class ImageCodeView(APIView):
    def get(self, request, image_code_id):
        text, image = captcha.generate_captcha()
        print(text)
        redis_conn = get_redis_connection('verify_codes')
        redis_conn.setex("img_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)

        return HttpResponse(image, content_type='image/jpg')


class SMSCodeView(GenericAPIView):
    serializer_class = ImageCodeCheckSerializer

    def get(self, request, mobile):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        sms_code = '%06d' % random.randint(0, 999999)
        print(sms_code)
        redis_conn = get_redis_connection('verify_codes')

        # redis管道
        pl = redis_conn.pipeline()
        pl.setex("sms_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex("send_flag_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)

        # 让管道通知redis执行命令
        pl.execute()

        expires = constants.SMS_CODE_REDIS_EXPIRES // 60
        send_sms_code.delay(mobile, sms_code, expires, constants.SMS_CODE_TEMP_ID)

        return Response({'message': 'OK'})
