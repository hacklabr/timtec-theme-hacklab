# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.views.generic import TemplateView
from rest_framework import routers

from . import views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'answer-notification', views.AnswerNotificationViewSet)
router.register(r'unread-notification', views.UnreadNotificationViewSet)

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="base.html")),
    url(r'^api/', include(router.urls)),
    url(r'^chat/?$', views.ChatScreenView.as_view(template_name="chat.html"), name='chat_screen'),
    url(r'^_chat/auth/$', views.RocketchatIframeAuthView.as_view(), name='rocketchat_iframe_auth'),
    # url(r'^cadastro/?$', views.SindsepSignupView.as_view(), name='sindsep_signup'),
    url(r'^cadastro/?$', views.SindsepLoginView.as_view(), name='sindsep_login'),
    url(r'^cadastro/ausente?$',
        TemplateView.as_view(template_name='account/sindsep_signup_error.html'),
        name='sindsep_signup_error'
        ),
]
