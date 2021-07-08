"""shoppingMall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from Mall import views

urlpatterns = [
    path('', views.login),
    path('admin/', views.admin),
    path('login/', views.login),
    path('sign/', views.sign),
    path('homepage/', views.homepage),
    path('personal_info/', views.personal_info),
    path('update_personal_info/', views.update_personal_info),
    path('logout/', views.logout),
    path('add_cart/', views.add_cart),
    path('cart/', views.cart),
    path('delete_cart/', views.delete_cart),
    path('buy_cart/', views.buy_cart),
    path('order/', views.order),
    path('order_detail/', views.order_detail),
    path('delete_order/', views.delete_order),
    path('search/', views.search),
    path('filtrate/', views.filtrate),
    path('add_goods/', views.add_goods),
    path('delete_goods/', views.delete_goods),
    path('update_goods_info/', views.update_goods_info),
    path('delete_user/', views.delete_user),
    path('add_admin/', views.add_admin),
]
