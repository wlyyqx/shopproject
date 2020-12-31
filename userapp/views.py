from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect

from cart.cartmanager import SessionCartManager
from utils.code import *  #验证码工具包
from django.views import View
from .models import *
from django.core.serializers import serialize
class RegisterViews(View):
    def get(self,request):
        return render(request, 'register.html')

    def post(self,request):
        #获取参数
        uname = request.POST.get('uname','')
        pwd = request.POST.get('pwd','')
        user = UserInfo.objects.create(uname=uname,pwd=pwd)
        #判断是否注册成功
        if user:
            #将用户信息存放在session对象
            request.session['user'] = user
            return HttpResponseRedirect('/user/center/')

        return HttpResponseRedirect('/user/register/')
        #插入数据库
class CheckUnameViews(View):
    def get(self,request):
        #获取请求参数
        uname = request.GET.get('uname','')

        #根据用户名去数据库中查询
        userList = UserInfo.objects.filter(uname=uname)

        flag = False

        #判断是否存在
        if userList:
            flag = True

        return JsonResponse({'flag':flag})


class CenterViews(View):
    def get(self,request):
        return render(request,'center.html')


class LogoutViews(View):
    def post(self,request):
        #删除session中的数据
        if "user" in request.session:
            del request.session['user']    #删除session里的user
        return JsonResponse({'delflag':True})


class LoginViews(View):
    def get(self,request):

        #获取请求参数
        red = request.GET.get('redirect','')
        if not red:
            return render(request,'login.html',{'redirect':red})
        return render(request,'login.html')
    def post(self,request):
        uname=request.POST.get('uname','')
        pwd=request.POST.get('pwd','')
        userList = UserInfo.objects.filter(uname=uname,pwd=pwd)

        if userList:
            request.session['user'] = userList[0]   #把uname存进session
            red = request.POST.get('redirect','')
            if  red=='cart':
                #将session的购物项移动到数据库
                SessionCartManager(request.session).migrateSession2DB()
                return HttpResponseRedirect('/cart/queryAll/')
            elif red =='order':
                return  HttpResponseRedirect('/order/order.html?cartitems='+request.POST.get('cartitems',''))

            request.session['user'] = userList[0]
            return HttpResponseRedirect('/cart/queryAll/')
        return HttpResponseRedirect('/user/login/')


class LoadCodeViews(View):
    def get(self,request):
        img,str=gene_code()
        #将生成的验证码存放在session中
        request.session['sessioncode'] = str
        return HttpResponse(img,content_type='image/png')


class CheckcodeViews(View):
    def get(self,request):
        #获取输入框验证码
        code = request.GET.get('code','')
        #获取生成的验证码
        sessioncode = request.session.get('sessioncode',None)
        #比较是否相等
        flag = code == sessioncode
        return JsonResponse({'checkFlag':flag})


class AddressViews(View):
    def get(self,request):
        user = request.session.get('user', '')
        addrList = user.address_set.all
        return render(request, 'address.html', {'addrlist': addrList})

    def post(self,request):
        #获取请求参数
        aname=request.POST.get('aname','')
        aphone=request.POST.get('aphone','')
        addr=request.POST.get('addr')
        #从session中获取user
        user = request.session.get('user','')
        address= Address.objects.create(aname=aname,aphone=aphone,addr=addr,userinif=user,isdefault=(lambda count: True if count == 0 else False)(user.address_set.all().count()))

        #获取当前用户的所有收获地址
        addrList = user.address_set.all
        return render(request,'address.html',{'addrlist':addrList})

class LoadAreaViews(View):
    def get(self,request):
        #获取请求参数
        pid = request.GET.get('pid',1)
        pid = int(pid)
        #根据父id查询区划信息
        arealist = Area.objects.filter(parentid=pid)
        #进行序列化(吧对象转换字符串)
        jarealist = serialize('json',arealist)

        return JsonResponse({'jareaList':jarealist})