#coding=utf-8
from goods.models import *
from django.db.transaction import atomic  #事务

@atomic
def test_model():
    with open('utils/jiukuaijiu.json') as fr:  #打开文件
        import json
        datas = json.loads(fr.read())  #将json转化为对象
        for data in datas:  #循环列表
            #data[xxx]用keys 获取value

            cate = Category.objects.create(cname=data['category'])  #添加数据

            _goods = data['goods'] #循环列表

            for goods in _goods:  #循环列表 往goods添加数据
                good = Goods.objects.create(gname=goods['goodsname'], gdesc=goods['goods_desc'],
                                            price=goods['goods_price'], oldprice=goods['goods_oldprice'],
                                            category=cate) #category外键
                sizes = []
                for _size in goods['sizes']:
                    if Size.objects.filter(sname=_size[0]).count() == 1:
                        size = Size.objects.get(sname=_size[0])
                    else:
                        size = Size.objects.create(sname=_size[0])
                    sizes.append(size)

                colors = []
                for _color in goods['colors']:
                    color = Color.objects.create(colorname=_color[0], colorurl=_color[1])
                    colors.append(color)

                for _spec in goods['specs']:
                    goodsdetails = GoodsDetailName.objects.create(gdname=_spec[0])
                    for img in _spec[1]:
                        GoodsDetail.objects.create(goods=good,gdname=goodsdetails,gdurl=img)

                for c in colors:
                    for s in sizes:
                        Inventory.objects.create(count=100,goods=good, color=c, size=s)




def deleteall():
    Category.objects.filter().delete()
    Color.objects.filter().delete()
    Size.objects.filter().delete()

