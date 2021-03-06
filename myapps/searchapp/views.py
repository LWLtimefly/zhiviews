import json
import logging

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from BestJob.utils import rds
from searchapp import views_chars
from userapp.models import User
from searchapp.models import JobMsg, JobCitys
from django.core.cache import cache
from django.views.decorators.cache import cache_page


def home(request):
    # 主页接口
    # 获取所有城市
    citys = [city[0] for city in JobCitys.objects.all().values_list('cityname')]
    citys = tuple(citys)
    # 获取登录用户token
    tok = request.session.get('login_user')
    data = {}
    if tok:
        data['username'] = User.objects.get(token=tok).username
        if not User.objects.get(token=tok).image:
            data['photo'] = '1.png'
        else:
            data['photo'] = User.objects.get(token=tok).image
    return render(request, 'home.html', {'data': data, 'citys': citys})


def changecity(request):
    # 切换城市
    return None


@cache_page(60)
def search(request):
    # 获取登录用户token
    tok = request.session.get('login_user')
    if not tok:
        return redirect('/user/login/')

    city = request.GET.get('cityKw', None)
    if city != '全国':
        city_id = JobCitys.objects.get(cityname=city).cityid
    else:
        city_id = '全国'
    job = request.GET.get('jobKw', '')

    # 获取所有城市
    citys = [city[0] for city in JobCitys.objects.all().values_list('cityname')]
    citys = tuple(citys)

    # 获取登录用户token
    tok = request.session.get('login_user')
    data = {}
    if tok:
        data['username'] = User.objects.get(token=tok).username
        if not User.objects.get(token=tok).image:
            data['photo'] = '1.png'
        else:
            data['photo'] = User.objects.get(token=tok).image

    zhiwei = zhiweitable(city, job)

    # 公司热度排行（前10）
    topCompany = getCompanyTop(10)

    content = views_chars.index(city_id, job, 'time')
    # print('打印：',content)
    # print('类型:',type(content))
    content['data'] = data
    content['zhiwei'] = zhiwei
    content['citys'] = citys
    content['topCompany'] = topCompany
    content['search_city_id'] = city_id
    #print('选择的工作:', job)
    if not job:
        content['job'] = 'WU'
        # print('eeeeeeeeee',content['job'])
    else:
        content['job'] = job
    return render(request, 'smallsearch.html', content)




def search_chart(request):
    city = request.GET.get('search_city_id')
    job = request.GET.get('job')

    title_type = request.GET.get('title')
    # print('城市id：', city)
    # print('工作:', job)
    # print('图形类型：', title_type)
    if job == 'WU':
        chart = views_chars.index(city, '', title_type)
    else:
        chart = views_chars.index(city, job, title_type)
    # print(type(chart))
    # print('查询:',chart)
    return JsonResponse(chart)


def zhiweitable(city, job):
    if city == '全国':
        zhiwei = JobMsg.objects.filter(job_name__icontains=job).all()
    else:
        zhiwei = JobCitys.objects.get(cityname=city).jobmsg_set.filter(job_name__icontains=job).all()

    return zhiwei


# 公司详情
def xiangxi(request, id):
    # 获取登录用户token
    tok = request.session.get('login_user')
    if not tok:
        return redirect('/user/login/')

    # 获取所有城市
    citys = [city[0] for city in JobCitys.objects.all().values_list('cityname')]
    citys = tuple(citys)

    data = {}
    if tok:
        data['username'] = User.objects.get(token=tok).username
        if not User.objects.get(token=tok).image:
            data['photo'] = '1.png'
        else:
            data['photo'] = User.objects.get(token=tok).image

    job = JobMsg.objects.filter(id=id).first()
    if job:
        # 将被点击的公司写入到排行中
        rds.zincrby('companyTop', id, 1)
        return render(request, 'xiangxi.html', {'job': job, 'data': data, 'citys': citys})

    return HttpResponse('<p>很抱歉，此公司暂无详细信息！</p>')


# 排行榜
# @cache_page(10)
def getCompanyTop(n):
    topn = rds.zrevrange('companyTop', 0, n - 1, withscores=True)
    print(topn)
    ids = [int(id) for id, score in topn]
    companys = JobMsg.objects.in_bulk(ids)
    companys_top = [(companys.get(int(id)), int(score)) for id, score in topn]
    return companys_top
