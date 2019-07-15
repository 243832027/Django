from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameView.as_view()),
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileView.as_view()),
    url(r'^users/$', views.UserView.as_view()),

]
