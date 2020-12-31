#全局上下文:所有前端页面都可共享getUserinfo的数据

def getUserinfo(request):
    #返回susers 储存在session的用户名
    return {
        'suser':request.session.get('user',None)
    }