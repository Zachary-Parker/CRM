import json
import datetime
from django.conf.urls import url
from django.db.models import Q
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.shortcuts import render,HttpResponse,redirect
from django.forms import ModelForm
from django.db import transaction

from crm import models
from stark.service import v1
from utils import message
from crm.permissions.customer import CustomerPersmission

class SingleModelForm(ModelForm):
    class Meta:
        model = models.Customer
        exclude = ['consultant','status','recv_date','last_consult_date']



class CustomerConfig(CustomerPersmission,v1.StarkConfig):
    order_by = ['-status']

    def display_gender(self,obj=None,is_header=False):
        if is_header:
            return '性别'
        return obj.get_gender_display()

    def display_education(self,obj=None,is_header=False):
        if is_header:
            return '学历'
        return obj.get_education_display()

    def display_course(self,obj=None,is_header=False):
        if is_header:
            return '咨询课程'
        course_list = obj.course.all()
        html = []
        # self.request.GET
        # self._query_param_key
        # 构造QueryDict
        # urlencode()
        for item in course_list:
            temp = "<a style='display:inline-block;padding:3px 5px;border:1px solid blue;margin:2px;' href='/stark/crm/customer/%s/%s/dc/'>%s X</a>" %(obj.pk,item.pk,item.name)
            html.append(temp)

        return mark_safe("".join(html))

    def display_status(self,obj=None,is_header=False):
        if is_header:
            return '状态'
        return obj.get_status_display()

    def record(self,obj=None,is_header=False):
        if is_header:
            return '跟进记录'
        # /stark/crm/consultrecord/?customer=11
        return mark_safe("<a href='/stark/crm/consultrecord/?customer=%s'>查看跟进记录</a>" %(obj.pk,))

    list_display = ['qq','name',display_gender,display_education,display_course, 'consultant', display_status,record]
    edit_link = ['qq']



    def delete_course(self,request,customer_id,course_id):
        """
        删除当前用户感兴趣的课程
        :param request: 
        :param customer_id: 
        :param course_id: 
        :return: 
        """
        customer_obj = self.model_class.objects.filter(pk=customer_id).first()
        customer_obj.course.remove(course_id)
        # 跳转回去时，要保留原来的搜索条件
        return redirect(self.get_list_url())

    def extra_url(self):
        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        patterns = [
            url(r'^(\d+)/(\d+)/dc/$', self.wrap(self.delete_course), name="%s_%s_dc" %app_model_name),
            url(r'^public/$', self.wrap(self.public_view), name="%s_%s_public" %app_model_name),
            url(r'^user/$', self.wrap(self.user_view), name="%s_%s_user" %app_model_name),
            url(r'^(\d+)/competition/$', self.wrap(self.competition_view), name="%s_%s_competition" %app_model_name),
            url(r'^single/$', self.wrap(self.single_view), name="%s_%s_single" %app_model_name),
            url(r'^multi/$', self.wrap(self.multi_view), name="%s_%s_multi" %app_model_name),
        ]
        return patterns

    def public_view(self,request):
        """
        公共客户资源
        :param request: 
        :return: 
        """
        current_user_id = 6

        ctime = datetime.datetime.now().date()
        no_deal = ctime - datetime.timedelta(days=15)  # 接客
        no_follow = ctime - datetime.timedelta(days=3) # 最后跟进日期

        customer_list = models.Customer.objects.filter(Q(recv_date__lt=no_deal)|Q(last_consult_date__lt=no_follow),status=2)
        return render(request,'public_view.html',{'customer_list':customer_list,'current_user_id':current_user_id})

    def competition_view(self,request,cid):
        """
        抢单
        :param request: 
        :param nid: 
        :return: 
        """
        current_user_id = 6
        ctime = datetime.datetime.now().date()
        no_deal = ctime - datetime.timedelta(days=15)  # 接客
        no_follow = ctime - datetime.timedelta(days=3)  # 最后跟进日期

        row_count = models.Customer.objects.filter(Q(recv_date__lt=no_deal) | Q(last_consult_date__lt=no_follow), status=2,id=cid).exclude(consultant_id=current_user_id).update(recv_date=ctime,last_consult_date=ctime,consultant_id=current_user_id)
        if not row_count:
            return HttpResponse('手速太慢了')

        models.CustomerDistribution.objects.create(user_id=current_user_id,customer_id=cid,ctime=ctime)

        return HttpResponse('抢单成功')


    def user_view(self,request):
        """
        当前登录用户的所有客户
        :param request: 
        :return: 
        """
        # 去session中获取当前登录用户ID
        current_user_id = 6

        # 当前用户的所有客户列表
        customers = models.CustomerDistribution.objects.filter(user_id=current_user_id).order_by('status')

        return render(request,'user_view.html',{'customers':customers})


    def single_view(self,request):
        """
        单条录入客户信息
        :param request: 
        :return: 
        """

        if request.method == "GET":
            form = SingleModelForm()
            return render(request,'single_view.html',{'form':form})
        else:
            """单条导入，request.POST所有导入的数据
              一、数据校验
              二、获取销售ID
              三、写入数据库
            """
            form = SingleModelForm(request.POST)
            # 数据校验
            if form.is_valid():
                from xxxxxx import AutoSale
                ctime = datetime.datetime.now().date()

                # 获取销售ID
                sale_id = AutoSale.get_sale_id()
                if not sale_id:
                    return HttpResponse("无销售顾问，无法进行自动分配")

                try:
                    with transaction.atomic():
                        # 创建客户表
                        form.instance.consultant_id = sale_id
                        form.instance.recv_date = ctime
                        form.instance.last_consult_date = ctime
                        new_customer = form.save()

                        # 创建客户分配表
                        models.CustomerDistribution.objects.create(customer=new_customer,user_id = sale_id,ctime=ctime)


                        # 发送消息
                        message.send_message('877252373@qq.com','放哨','你别走了','三个月工资太多了')

                except Exception as e:
                    # 创建客户和分配销售异常
                    AutoSale.rollback(sale_id)
                    return HttpResponse('录入异常')

                return HttpResponse('录入成功')

            else:
                return render(request, 'single_view.html', {'form': form})


    def multi_view(self,request):
        """
        批量导入
        :param request: 
        :return: 
        """
        if request.method == 'GET':
            return render(request,'multi_view.html')
        else:
            from django.core.files.uploadedfile import InMemoryUploadedFile
            file_obj = request.FILES.get('exfile')
            with open('xxxxxx.xlsx',mode='wb') as f:
                for chunk in file_obj:
                    f.write(chunk)
            # 作业2：不在创建临时 xxxxxx.xlsx 文件
            import xlrd
            workbook = xlrd.open_workbook('xxxxxx.xlsx')
            # sheet_names = workbook.sheet_names()
            # sheet = workbook.sheet_by_name('工作表1')
            sheet = workbook.sheet_by_index(0)
            maps = {
                0:'name',
                1:'qq',
            }

            for index in range(1,sheet.nrows):
                row = sheet.row(index)
                # {'name':"吧唧",'qq':9898}
                # print(row,type(row))
                row_dict = {}
                for i in range(len(maps)):
                    key = maps[i]
                    cell = row[i]
                    row_dict[key] = cell.value
                print(row_dict)
                # 自动获取ID
                # 录入客户表
                # 录入客户分配表
            return HttpResponse('上传成功')














