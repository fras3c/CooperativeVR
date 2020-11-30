from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
           path('', views.index, name='index'),
           path('demo/', views.demo, name='demo'),
           path('cooperation/', views.cooperation, name='cooperation'),
           #path('solve/', views.solve, name='solve'),
           path('upload/', views.upload, name='upload'),
           path('manual/', views.manual, name='manual'),
           # url(r'', views.default_map, name="default"),
           # url(r'^demo/$', views.demo, name='demo'),
            ]
