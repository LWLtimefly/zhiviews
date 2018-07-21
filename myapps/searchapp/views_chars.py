from django.shortcuts import render

# Create your views here.

# from __future__ import unicode_literals

import math
from pyecharts import Map
from django.http import HttpResponse
from django.template import loader
from pyecharts import Line3D
from pyecharts import Bar
from pyecharts import EffectScatter
import numpy as np
from pandas import DataFrame, Series
import pandas as pd
from pyecharts import Geo
from pyecharts import Bar, Timeline
from random import randint

# 查询数据
from searchapp.models import JobMsg,JobCitys
from pyecharts import Bar, Line, Timeline, Overlap
from django.views.decorators.cache import cache_page

'''如
w = models.Simp.objects.all().values_list('username')
print w, type(w)

[(u'chenc',), (u'zan',), (u'zhangsan',)] <class 'django.db.models.query.QuerySet'>



w = models.Simp.objects.all().values_list('id', 'username')
print w, type(w)

[(1, u'chenc'), (2, u'zan'), (3, u'zhangsan')] <class 'django.db.models.query.QuerySet'>

'''

# 划分等级   0-2000   2000-4000   4000-6000 6000-8000 8000-10000   10000-15000  150000-20000  20000-30000 30000以上


# 饼图
from pyecharts import Pie

# 折线图
from pyecharts import Line
# from __future__ import unicode_literals
from pyecharts import Bar, Line, Grid
from pyecharts import Boxplot
from pyecharts import Page
import nltk
import jieba
from pyecharts import WordCloud
from collections import Counter

'''
    # add()中的参数
    title = ''  # 主标题


'''


def maps(city):
    # # ---------------------------------------薪资频数分布图-----------------------------------
    # #
    # #
    # # 饼图  薪资频数分布图
    if city == '全国':
        a = list(JobMsg.objects.all().values_list('job_meanmoney', ))
    else:
        a = list(JobMsg.objects.filter(job_address=city).values_list('job_meanmoney', ))
    # print(a)
    mm = {'0-2000':0,'2000-4000':0,'4000-6000':0,'6000-8000':0,'8000-10000':0,'10000-15000':0,'15000-20000':0,'20000-30000':0,'30000以上':0}
    for i in a:
        if int(i[0]) < 2000:
            mm['0-2000']+=1
        elif int(i[0]) < 4000:
            mm['2000-4000']+=1
        elif int(i[0]) < 6000:
            mm['4000-6000']+=1
        elif int(i[0]) < 8000:
            mm['6000-8000']+=1
        elif int(i[0]) < 10000:
            mm['8000-10000']+=1
        elif int(i[0]) < 15000:
            mm['10000-15000']+=1
        elif int(i[0]) < 20000:
            mm['15000-20000']+=1
        elif int(i[0]) < 30000:
            mm['20000-30000']+=1
        else:
            mm['30000以上']+=1

    # ss = {}
    # for i in mm:
    #     if mm.count(i) >= 1:
    #         ss[i] = mm.count(i)
    key = list(mm.keys())
    value = list(mm.values())
    pie = Pie(title="薪资所占比例图", title_pos='left', width=1000, height=350, title_text_size=18)
    # pie.add(
    #     "",
    #     key,
    #     value,
    #     radius=[35, 60],
    #     center=[65, 50],
    #     legend_pos="80%",
    #     legend_orient="vertical",
    # )

    # 选图
    # pie.add("", key, value, radius=[35, 50], label_text_color=None, title_pos='left',
    #         is_label_show=True, legend_orient='vertical')
    #
    # pie.add("商品A", key, value, center=[65, 50], is_random=True,
    #         radius=[35, 50], rosetype='radius', legend_pos='left', legend_orient='vertical')

    pie.add("薪资频数分布图", key, value, center=[45, 50], is_random=True,
            radius=[35, 60], rosetype='area', legend_pos='left', legend_orient='vertical',
            is_legend_show=False, is_label_show=True)
    return pie
    #
    # grid = Grid()
    # grid.add(line, grid_right="55%")
    # grid.add(pie, grid_left="55%")
    # return grid
    # page.add(pie)

from pyecharts import Geo

#@cache_page(60)
def line3d():
    # --------------------地图---------------------------------
    a = list(JobMsg.objects.all().values_list('job_address'))
    # print(a)
    city_names=[]
    for city_id in a:
        try:
            city_names.append(JobCitys.objects.get(cityid=city_id[0]).cityname)

        except:
            pass
    ss = {}

    for i in city_names:
        if city_names.count(i) >= 1:
            ss[i] = city_names.count(i)
    print(ss)
    hh = []
    for i, j in ss.items():
        if i not in ['丽江']:
            hh.append((i, j))
    # print(hh)

    geo = Geo("城市与需求量关系图", title_color="#fff",
              title_pos="center", width=1000,
              height=600, background_color='#404a59')
    attr, value = geo.cast(hh)
    geo.add("", attr, value, visual_range=[0, 200], visual_text_color="#fff",
            symbol_size=15, is_visualmap=True)
    return geo

    # ----------------------------------词云图-------------------------------------------
    # ci = list(JobMsg.objects.all().values_list('job_zwtext', ))
    # ci = ci[0:5]
    # # print(ci)
    #
    # # ci = [(
    # #     "岗位职责 1. 负责计算机视觉、图像处理相关算法的研发和优化； 2. 深入分析现有算法，了解业务需求，给出有效的优化解决方案； 3. 跟踪业界学界前沿算法最新进展。 任职要求1. 计算机、电子、统计及数学等专业； 2. 了解机器学习、计算机视觉或图像处理； 3. 熟练使用Python，熟悉至少一种深度学习框架比如Caffe，TensorFlow, MXNet, (Py)Torch, 等 。代码能力较强，有C++和Java语言编程经验的优先。 4. 数理功底扎实，自学能力强",),
    # #     (
    # #         "岗位描述： 1、负责前端产品线的工程化建设和开发规范的制定2、负责封装公用组件和优化系统架构3、与系统工程师、设计师密切合作，参与产品需求、产品设计，负责开发实现以及测试、维护等迭代周期岗位要求： 1、熟练掌握 HTML、CSS、JavaScript 等前端基础技术2、熟练掌握至少一种 HTML 模板语言如 Jinja、Smarty、Velocity、Jade、Mustache 等",), ]
    #
    # cici = []
    # for i in ci:
    #     cici.append(i[0])
    # c = ''
    # ciyu = c.join(cici)
    # a = list(jieba.cut(ciyu))
    # stripa = []
    # for i in a:
    #     stripa.append(i.strip(" "))
    #
    # # 停词表
    # stopwords = []
    # for word in open('/Users/lili/后两周课/StopWords.txt', 'r', encoding='gbk'):
    #     stopwords.append(word.strip())
    #
    # for i in stripa:
    #     if i in stopwords:
    #         stripa.remove(i)
    # # print(stripa)
    # cfd = nltk.FreqDist(a)
    # cipin = list(cfd.keys())
    # fre = list(cfd.values())
    # # print(cipin)
    #
    # wordcloud = WordCloud('词云图', width=500, height=350)
    # wordcloud.add("", cipin, fre, word_size_range=[20, 100])
    # # print(wordcloud)
    # return wordcloud
    # page.add(wordcloud)
    # return page

    #
    # names = [
    #     'Sam S Club', 'Macys', 'Amy Schumer', 'Jurassic World', 'Charter Communications',
    #     'Chick Fil A', 'Planet Fitness', 'Pitch Perfect', 'Express', 'Home', 'Johnny Depp',
    #     'Lena Dunham', 'Lewis Hamilton', 'KXAN', 'Mary Ellen Mark', 'Farrah Abraham',
    #     'Rita Ora', 'Serena Williams', 'NCAA baseball tournament', 'Point Break']
    # values = [
    #     10000, 6181, 4386, 4055, 2467, 2244, 1898, 1484, 1112,
    #     965, 847, 582, 555, 550, 462, 366, 360, 282, 273, 265]
    # wordcloud = WordCloud(width=1300, height=620)
    # wordcloud.add("", names, values, word_size_range=[30, 100],
    #               shape='diamond', width=500, height=350)
    # page = Page()
    # page.add(geo)
    # page.add(wordcloud)
    # return page
    # # return wordcloud

    #
    # # -----------------------------工作经验的平均薪资的关系图----------------------------


def line(city):
    if city == '全国':
        a = list(JobMsg.objects.all().values_list('job_jy', 'job_meanmoney'))
    else:
        a = list(JobMsg.objects.filter(job_address=city).values_list('job_jy', 'job_meanmoney'))
    print(a)
    exprice = []
    for i in a:
        exprice.append([i[0], int(i[1])])
    print(exprice)

    exprice = DataFrame(exprice)
    sss = Series(exprice.groupby(0).mean()[1])
    # print(sss)
    index1 = list(sss.index)
    # print(index1)
    value1 = list(sss.values)
    # print(value1)
    b = list(zip(index1, value1))
    a = [['1经验不限', 0], ['2应届生', 0], ['31年以内', 0], ['41-3年', 0], ['53-5年', 0], ['65-10年', 0], ['710年以上', 0]]
    for i in b:
        for j in a:
            if j[0][1:] == i[0]:
                j[1] = i[1]
    lkey = []
    lvalue = []
    for i in a:
        lkey.append(i[0][1:])
        lvalue.append(round(i[1], 2))
    # print('----------------')
    # print(lkey)
    # print(lvalue)

    line = Bar('工作经验与平均薪资柱子图', width=1000, height=350, title_text_size=16, title_pos='left')
    line.add('工作经验', lkey, lvalue, area_color='#000',
             is_stack=True, is_label_show=True, is_smooth=True,
             xaxis_name='工作经验')
    return line
    # page.add(line)
    # return line

    # --------------------------------学历与平均薪资的箱线图--------------------------------


def edu(city):
    if city == '全国':
        e = list(JobMsg.objects.all().values_list('job_xl', 'job_meanmoney'))
    else:
        e = list(JobMsg.objects.filter(job_address=city).values_list('job_xl', 'job_meanmoney'))
    # print(e)
    ee = []
    for i in e:
        ee.append([i[0], int(i[1])])
    # print(ee)

    edu = DataFrame(ee)
    edulist = {}
    for i in edu[0]:
        edulist[i] = list(edu.loc[edu[0] == i][1])

    k = []
    v = []
    for key, value in edulist.items():
        k.append(key)
        v.append(value)

    # print(k)
    # print('----',v)
    boxplot = Boxplot("学历与薪资水平箱线图", background_color='#', width=1000, height=350, title_text_size=18)
    _v = boxplot.prepare_data(v)  # 转换数据
    # print(_v)
    boxplot.add("boxplot", k, _v, xaxis_name='学历')
    return boxplot
    # page.add(boxplot)
    # return boxplot

    # ----------------------------------------------- 招聘需求词云图 ----------------------------------------------
    # Django返回的查询结果：

#
# def ciyun():
    # ci = [(
    #     "岗位职责 1. 负责计算机视觉、图像处理相关算法的研发和优化； 2. 深入分析现有算法，了解业务需求，给出有效的优化解决方案； 3. 跟踪业界学界前沿算法最新进展。 任职要求1. 计算机、电子、统计及数学等专业； 2. 了解机器学习、计算机视觉或图像处理； 3. 熟练使用Python，熟悉至少一种深度学习框架比如Caffe，TensorFlow, MXNet, (Py)Torch, 等 。代码能力较强，有C++和Java语言编程经验的优先。 4. 数理功底扎实，自学能力强",),
    #     (
    #         "岗位描述： 1、负责前端产品线的工程化建设和开发规范的制定2、负责封装公用组件和优化系统架构3、与系统工程师、设计师密切合作，参与产品需求、产品设计，负责开发实现以及测试、维护等迭代周期岗位要求： 1、熟练掌握 HTML、CSS、JavaScript 等前端基础技术2、熟练掌握至少一种 HTML 模板语言如 Jinja、Smarty、Velocity、Jade、Mustache 等",), ]
    #
    # cici = []
    # for i in ci:
    #     cici.append(i[0])
    # c = ''
    # ciyu = c.join(cici)
    # a = list(jieba.cut(ciyu))
    # stripa = []
    # for i in a:
    #     stripa.append(i.strip(" "))
    #
    # # 停词表
    # stopwords = []
    # for word in open('/Users/lili/后两周课/StopWords.txt', 'r', encoding='gbk'):
    #     stopwords.append(word.strip())
    #
    # for i in stripa:
    #     if i in stopwords:
    #         stripa.remove(i)
    # # print(stripa)
    # cfd = nltk.FreqDist(a)
    # cipin = list(cfd.keys())
    # fre = list(cfd.values())
    # # print(cipin)
    #
    # wordcloud = WordCloud('词云图', width=1300, height=620)
    # wordcloud.add("", cipin, fre, word_size_range=[20, 100])
    # # print(wordcloud)
    # return wordcloud
    # # page.add(wordcloud)
    # # return page
    # # return wordcloud



# ------------------------------------------------测试  时间轮播---------------------------------------------
def time(city):
    if city == '全国':
        lb = list(JobMsg.objects.all().values_list('job_xl', 'job_time'))
    else:
        lb = list(JobMsg.objects.filter(job_address=city).values_list('job_xl', 'job_time'))
    # print(lb)
    a = []
    b = []
    c = []
    for i in lb:
        a.append(i[0])
        b.append(int(i[1].split('-')[1]))
        c.append(int(i[1].split('-')[2]))

    # print(a)
    # print(b)
    cc = list(zip(a, b, c))
    t = DataFrame(cc)
    k = ['高中', "中专/中技", "大专", "本科", "硕士", "不限"]
    # print(list(Series(t.loc[(t[1] == 3) & (t[2] < 8)][0]).values))

    bar_1 = Bar('三 月')
    bar_11_w = list(Series(t.loc[(t[1] == 3) & (t[2] < 8)][0]).values)
    bar_11_s = []
    for i in k:
        bar_11_s.append(bar_11_w.count(i))
    bar_1.add("week 1", k, bar_11_s)

    bar_12_w = list(Series(t.loc[(t[1] == 3) & (t[2] > 8) & (t[2] < 15)][0]).values)
    bar_12_s = []
    for i in k:
        bar_12_s.append(bar_12_w.count(i))
    bar_1.add("week 2", k, bar_12_s)

    bar_13_w = list(Series(t.loc[(t[1] == 3) & (t[2] > 15) & (t[2] < 21)][0]).values)
    bar_13_s = []
    for i in k:
        bar_13_s.append(bar_13_w.count(i))
    bar_1.add("week 3", k, bar_13_s)

    bar_14_w = list(Series(t.loc[(t[1] == 3) & (t[2] > 21) & (t[2] < 31)][0]).values)
    bar_14_s = []
    for i in k:
        bar_14_s.append(bar_14_w.count(i))
    bar_1.add("week 4", k, bar_14_s)

    bar_2 = Bar('四 月')
    bar_21_w = list(Series(t.loc[(t[1] == 4) & (t[2] < 8)][0]).values)
    bar_21_s = []
    for i in k:
        bar_21_s.append(bar_21_w.count(i))
    bar_2.add("week 1", k, bar_21_s)

    bar_22_w = list(Series(t.loc[(t[1] == 4) & (t[2] > 8) & (t[2] < 15)][0]).values)
    bar_22_s = []
    for i in k:
        bar_22_s.append(bar_22_w.count(i))
    bar_2.add("week 2", k, bar_22_s)

    bar_23_w = list(Series(t.loc[(t[1] == 4) & (t[2] > 15) & (t[2] < 21)][0]).values)
    bar_23_s = []
    for i in k:
        bar_23_s.append(bar_23_w.count(i))
    bar_2.add("week 3", k, bar_23_s)

    bar_24_w = list(Series(t.loc[(t[1] == 4) & (t[2] > 21) & (t[2] < 31)][0]).values)
    bar_24_s = []
    for i in k:
        bar_24_s.append(bar_24_w.count(i))
    bar_2.add("week 4", k, bar_24_s)

    bar_3 = Bar('五 月')
    bar_31_w = list(Series(t.loc[(t[1] == 5) & (t[2] < 8)][0]).values)
    bar_31_s = []
    for i in k:
        bar_31_s.append(bar_31_w.count(i))
    bar_3.add("week 1", k, bar_31_s)

    bar_32_w = list(Series(t.loc[(t[1] == 5) & (t[2] > 8) & (t[2] < 15)][0]).values)
    bar_32_s = []
    for i in k:
        bar_32_s.append(bar_32_w.count(i))
    bar_3.add("week 2", k, bar_32_s)

    bar_33_w = list(Series(t.loc[(t[1] == 5) & (t[2] > 15) & (t[2] < 21)][0]).values)
    bar_33_s = []
    for i in k:
        bar_33_s.append(bar_33_w.count(i))
    bar_3.add("week 3", k, bar_33_s)

    bar_34_w = list(Series(t.loc[(t[1] == 5) & (t[2] > 21) & (t[2] < 31)][0]).values)
    bar_34_s = []
    for i in k:
        bar_34_s.append(bar_34_w.count(i))
    bar_3.add("week 4", k, bar_34_s)

    bar_4 = Bar('六 月')
    bar_41_w = list(Series(t.loc[(t[1] == 6) & (t[2] < 8)][0]).values)
    bar_41_s = []
    for i in k:
        bar_41_s.append(bar_41_w.count(i))
    bar_4.add("week 1", k, bar_41_s)

    bar_42_w = list(Series(t.loc[(t[1] == 6) & (t[2] > 8) & (t[2] < 15)][0]).values)
    bar_42_s = []
    for i in k:
        bar_42_s.append(bar_42_w.count(i))
    bar_4.add("week 2", k, bar_42_s)

    bar_43_w = list(Series(t.loc[(t[1] == 6) & (t[2] > 15) & (t[2] < 21)][0]).values)
    bar_43_s = []
    for i in k:
        bar_43_s.append(bar_43_w.count(i))
    bar_4.add("week 3", k, bar_43_s)

    bar_44_w = list(Series(t.loc[(t[1] == 6) & (t[2] > 21) & (t[2] < 31)][0]).values)
    bar_44_s = []
    for i in k:
        bar_44_s.append(bar_44_w.count(i))
    bar_4.add("week 4", k, bar_44_s)

    bar_5 = Bar('七 月')
    bar_51_w = list(Series(t.loc[(t[1] == 7) & (t[2] < 8)][0]).values)
    bar_51_s = []
    for i in k:
        bar_51_s.append(bar_51_w.count(i))
    bar_5.add("week 1", k, bar_51_s)

    bar_52_w = list(Series(t.loc[(t[1] == 7) & (t[2] > 8) & (t[2] < 15)][0]).values)
    bar_52_s = []
    for i in k:
        bar_52_s.append(bar_52_w.count(i))
    bar_5.add("week 2", k, bar_52_s)

    bar_53_w = list(Series(t.loc[(t[1] == 7) & (t[2] > 15) & (t[2] < 51)][0]).values)
    bar_53_s = []
    for i in k:
        bar_53_s.append(bar_53_w.count(i))
    bar_5.add("week 3", k, bar_53_s)

    bar_54_w = list(Series(t.loc[(t[1] == 7) & (t[2] > 51) & (t[2] < 31)][0]).values)
    bar_54_s = []
    for i in k:
        bar_54_s.append(bar_54_w.count(i))
    bar_5.add("week 4", k, bar_54_s, is_legend_show=True)
    timeline = Timeline(is_auto_play=True, timeline_bottom=0, width=1000, height=450)
    timeline.add(bar_1, '三 月')
    timeline.add(bar_2, '四 月')
    timeline.add(bar_3, '五 月')
    timeline.add(bar_4, '六 月')
    timeline.add(bar_5, '七 月')
    return timeline


REMOTE_HOST = "https://pyecharts.github.io/assets/js"


def index(request,city):
    # template = loader.get_template('myfirstvis/pyecharts.html')
    map = maps(city)
    l3d = line3d()
    l = line(city)
    e = edu(city)
    # c = ciyun()
    t = time(city)
    context = dict(
        maps=map.render_embed(),
        myechart=l3d.render_embed(),
        host=REMOTE_HOST,
        script_list=l3d.get_js_dependencies(),
        line=l.render_embed(),
        edu=e.render_embed(),
        # ciyun=c.render_embed(),
        time=t.render_embed(),
        script_list1=map.get_js_dependencies(),
        script_list2=l.get_js_dependencies(),
        # script_list3=c.get_js_dependencies(),

    )
    # print(context)
    # return HttpResponse(template.render(context, request))
    return context


# {'北京': 313, '广州': 184, '西安': 326, '南京': 25,
# '成都': 177, '保定': 1, '苏州': 1419, '开封': 1, '邯郸': 1,
#  '合肥': 7, '福州': 6, '厦门': 650, '武 1, '贵阳': 8,
# '台州': 1, '临沂': 1, '大连': 13, '株洲': 1, '重庆': 12,
# '烟台': 1, '上海': 449, '佛山': 5, '济南': 7, '扬州': 2,
# '东莞': 6, '无锡': 3, 8, '中山': 4, '南充': 2, '杭州': 788,
# '宁波': 8, '洛阳': 1, '南通': 2, '长春': 2, '南昌': 6,
# '衢州': 1, '宝鸡': 1, '温州': 3, '昆明': 5, '泰州': 1, ',
# '太原': 2, '唐山': 4, '湖州': 1, '张掖': 1, '珠海': 3,
# '济宁': 1, '廊坊': 1, '菏泽': 1, '德阳': 1, '惠州': 1,
#  '北海': 1, '枣庄': 1, '秦皇岛': 1, '酒': 2, '鄂州': 1,
# '天津': 136, '盐城': 1, '九江': 1, '蚌埠': 1, '漳州': 2,
#  '兰州': 1, '金华': 1, '六安': 1, '大庆': 1, '新余': 1,
# '乌鲁木齐': 1, '郑州'14, '海口': 1, '信阳': 1, '深圳': 427}
