from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
from django.views import View
from .cartmanager import *

class AddCartViews(View):
    def post(self,request):
        #在多级字典数据的时候,与要手动设置modified=True,实时地将数据村到session对象中
        request.session.modified = True


        #获取当前操作类型
        flag = request.POST.get('flag','')

        #判断当前操作类型
        if flag == 'add':
            #创建cartManage对象
            CartMangerObj = getCartManger(request)
            #加入购物车方法
            CartMangerObj.add(**request.POST.dict())

        elif flag == 'plus':
            #创建cartManage对象
            CartMangerObj = getCartManger(request)
            #修改商品数量
            CartMangerObj.update(step=1,**request.POST.dict())
        elif flag == 'minus':
            #创建cartManage对象
            CartMangerObj = getCartManger(request)
            #修改商品数量
            CartMangerObj.update(step=-1,**request.POST.dict())

        elif flag == 'delete':
            #创建cartManage对象
            CartMangerObj = getCartManger(request)
            #逻辑删除购物车选项
            CartMangerObj.delete(**request.POST.dict())


        return HttpResponseRedirect('/cart/queryAll/')


class CartListViews(View):
    def get(self,request):
        # 创建cartManage对象
        CartMangerObj = getCartManger(request)
        #查询所有购物信息
        cartlist = CartMangerObj.queryAll()
        return render(request,'cart.html',{'cartlist':cartlist})
