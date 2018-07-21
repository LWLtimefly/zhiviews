from django.http import HttpResponse
from django.shortcuts import render

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
    return render(request, 'home.html',{'data':data,'citys':citys})


def changecity(request):
    # 切换城市
    return None

@cache_page(60)
def search(request):
    print('##$%^&^%$#$%^&^%$#$%^&^%$#$%^&^%$#@#$%^&*()(#@#$%^&*&^%$')
    city = request.GET.get('cityKw','')
    if city != '全国':
        city_id = JobCitys.objects.get(cityname=city).cityid
    else:
        city_id = '全国'
    job = request.GET.get('jobKw','')

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

    zhiwei = zhiweitable(city,job)

    # 公司热度排行
    topCompany = getCompanyTop(15)

    content = views_chars.index(request,city_id)
    content['data'] = data
    content['zhiwei'] = zhiwei
    content['citys'] = citys
    content['topCompany'] = topCompany
    return render(request, 'smallsearch.html',content)


def zhiweitable(city,job):
    if city == '全国':
        zhiwei = JobMsg.objects.filter(job_name__icontains=job).all()
    else:
        zhiwei = JobCitys.objects.get(cityname=city).jobmsg_set.filter(job_name__icontains=job).all()
        # zhiwei = JobMsg.objects.filter(job_address= city,job_name__icontains=job).all()
    return zhiwei


# 公司详情
def xiangxi(request, id):
    job = JobMsg.objects.filter(id=id).first()
    if job:
        # 将被点击的公司写入到排行中
        rds.zincrby('companyTop',id, 1)
        return HttpResponse(job)

    return HttpResponse('<p>很抱歉，此公司暂无详细信息！</p>')


# 排行榜
#@cache_page(10)
def getCompanyTop(n):
    topn = rds.zrevrange('companyTop',0,n-1,withscores=True)
    print(topn)
    ids = [int(id) for id,score in topn]
    companys = JobMsg.objects.in_bulk(ids)
    companys_top = [(companys.get(int(id)),int(score)) for id,score in topn]
    return companys_top