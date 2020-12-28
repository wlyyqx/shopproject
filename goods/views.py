import math

from django.shortcuts import render
from .models import *
from django.views import View
from django.core.paginator import Paginator
from django.http import HttpResponse


class IndexViews(View):
    def get(self, request, cid=1, num=1):
        # 查询所有类别
        cates = Category.objects.all().order_by('id')  # 根据id分组
        # 根据类别查询所有信息
        goodslist = Goods.objects.filter(category_id=cid).order_by('id')
        # 分页(每页显示8条)
        pager = Paginator(goodslist, 8)
        # 获取当前页的数据
        page_list = pager.page(num)

        # 页码数
        begin = (num - int(math.ceil(10.0 / 2)))
        if begin < 1:
            begin = 1
        # 每页结束页码
        end = begin + 9
        if end > pager.num_pages:  # 越界判断,num_pages总页数
            end = pager.num_pages

        if end <= 10:
            begin = 1
        else:
            begin = end - 9

        pagelist = range(begin, end + 1)

        return render(request, 'index.html',
                      {'cates': cates, 'goodslist': page_list, 'cid': cid, 'pagelist': pagelist, 'currentNom': num})


# 猜你喜欢,装饰器
def recommend_view(func):
    def wrapper(detailViews, request, goodsid, *args, **kwargs):
        # 将存放在cookie中的goodsid获取
        cookie_str = request.COOKIES.get('recommend','')
        print(cookie_str)

        # 存放所有goodid的列表
        goodsidlist = [gid for gid in cookie_str.split() if gid.strip()]
        print(goodsidlist)
        # 最终需要获取的推荐商品
        goodsObjList = [Goods.objects.get(id=gsid) for gsid in goodsidlist if
                        gsid != goodsid and Goods.objects.get(id=gsid).category_id == Goods.objects.get(
                            id=goodsid).category_id][:4]
        print(goodsObjList)
        resp = func(detailViews, request, goodsid, goodsObjList, *args, **kwargs)

        # 判断goodsid是否存在goodsidlist中
        if goodsid in goodsidlist:
            goodsidlist.remove(goodsid)
            goodsidlist.insert(0, goodsid)
        else:
            goodsidlist.insert(0, goodsid)

        # 将goodsid中的数据保存到cookie中


        resp.set_cookie('recommend', ' '.join('%s' %id for id in goodsidlist), max_age=3 * 24 * 60 * 60)

        return resp

    return wrapper


class DetailViews(View):
    @recommend_view
    def get(self, request, goodsid, recommendlist=[]):
        # 根据goodsid查询商品详情信息(goodsid对象)
        goodsid=int(goodsid)
        goods = Goods.objects.get(id=goodsid)
        return render(request, 'detail.html', {'goods': goods, 'recommendlist': recommendlist})
