from django.shortcuts import render,HttpResponse,redirect
from crm import models
from django.db.models import Count

def test(request):

    # v1 = models.CustomerDistribution.objects.filter(ctime__year=2017, status=2).extra(
    #     select={'mt': 'strftime("%%Y-%%m",ctime)'}).values('mt').annotate(ct=Count('id'))
    # print(list(v1))
    #
    # v1 = [
    #     {'mt': '2017-12', 'ct': 3},
    #     {'mt': '2017-11', 'ct': 13},
    #     {'mt': '2017-10', 'ct': 15},
    #     {'mt': '2017-09', 'ct': 13},
    #     {'mt': '2017-08', 'ct': 63},
    #     {'mt': '2017-07', 'ct': 73},
    # ]
    #
    # v2 = [
    #     {'mt': '2017-12', 'ct': 13},
    #     {'mt': '2017-11', 'ct': 23},
    #     {'mt': '2017-10', 'ct': 25},
    #     {'mt': '2017-09', 'ct': 23},
    #     {'mt': '2017-08', 'ct': 73},
    #     {'mt': '2017-07', 'ct': 83},
    # ]

    start_date = "2017-10"
    end_date = "2017-12"
    all_list = models.CustomerDistribution.objects.filter(ctime__gte=start_date,ctime__lte=end_date,status=2).values('user_id','ctime')
    """
    [
        {'user_id':1, ctime: 2017-11-11,}
        {'user_id':1, ctime: 2017-11-11,}
        {'user_id':1, ctime: 2017-11-11,}
        {'user_id':1, ctime: 2017-11-12}
    ]
    
    
    [
        {
            name: '销售名称',
            data:[
                # [2017-11-01,5],
                [1501689804077.358, 1.0],
                [1501689804077.358, 1.0],
                [1501689804077.358, 1.0],
                [1501689804077.358, 1.0],
                [1501689804077.358, 1.0],
            ]
        },
        {
            name: '销售名1',
            data:[
                # [2017-11-01,5],
                [1501689804077.358, 1.0],
                [1501689804077.358, 1.0],
                [1501689804077.358, 1.0],
                [1501689804077.358, 1.0],
                [1501689804077.358, 1.0],
            ]
        }
    ]
    """



    return HttpResponse('...')

from rbac import models
from rbac.service.init_permission import init_permission
def login(request):
    if request.method == "GET":
        return render(request,'login.html')
    else:
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        user = models.User.objects.filter(username=user,password=pwd).first()
        print(user.userinfo)
        if user:
            # 表示已登录
            request.session['user_info'] = {'user_id':user.id,'uid':user.userinfo.id,'name':user.userinfo.name}
            # 权限写入session
            init_permission(user,request)
            # 跳转
            return redirect('/index/')
        print("3333")
        return render(request, 'login.html')



def index(request):
    return render(request,'index.html')











































