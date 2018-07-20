from django.db import models

# Create your models here.


# class CityName(models.Model):
#     id = models.IntegerField(primary_key=True,max_length=100,verbose_name='城市编号')
#     name=models.CharField(max_length=100,verbose_name='所在城市')
#
#
#
# class JobMsg(models.Model):
#     #岗位发布时间
#     job_time = models.CharField(max_length=100, blank=True, null=True)
#     #岗位名称
#     job_name = models.CharField(max_length=100, blank=True, null=True)
#     #岗位薪资
#     job_money = models.CharField(max_length=100, blank=True, null=True)
#     #平均薪资
#     job_meanmoney = models.CharField(db_column='job_meanMoney', max_length=100, blank=True, null=True)  # Field namemade lowercase.
#     #工作地点（多端定义）
#     job_address = models.ForeignKey(CityName,on_delete=models.SET_NULL)
#     #工作经验
#     job_jy = models.CharField(max_length=100, blank=True, null=True)
#     #学历
#     job_xl = models.CharField(max_length=100, blank=True, null=True)
#     #hr姓名
#     job_hrname = models.CharField(db_column='job_hrName', max_length=100, blank=True, null=True)  # Field name madelowercase.
#     #hr职位
#     job_hrleader = models.CharField(max_length=100, blank=True, null=True)
#     #职位简介
#     job_zwtext = models.TextField(blank=True, null=True)
#     #团队简介
#     job_tdtext = models.TextField(blank=True, null=True)
#     #公司简介
#     job_gstext = models.TextField(blank=True, null=True)
#     #公司名称
#     job_comname = models.CharField(db_column='job_comName', max_length=100, blank=True, null=True)  # Field name made lowercase.
#     #公司法人
#     company_username = models.CharField(db_column='company_userName', max_length=100, blank=True, null=True)  # Field name made lowercase.
#     #公司注册资金
#     company_money = models.CharField(max_length=100, blank=True, null=True)
#     #公司成立时间
#     company_time = models.CharField(max_length=100, blank=True, null=True)
#     #公司类型
#     company_type = models.CharField(max_length=100, blank=True, null=True)
#     #公司状态
#     company_status = models.CharField(max_length=100, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'job_msg'

class JobCitys(models.Model):
    cityname = models.CharField(db_column='cityName', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cityid = models.CharField(db_column='cityId', primary_key=True, max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'job_citys'

        verbose_name='城市信息'
        verbose_name_plural=verbose_name

class JobMsg(models.Model):
    job_time = models.CharField(max_length=100, blank=True, null=True)
    job_name = models.CharField(max_length=100, blank=True, null=True)
    job_money = models.CharField(max_length=100, blank=True, null=True)
    job_meanmoney = models.CharField(db_column='job_meanMoney', max_length=100, blank=True, null=True)  # Field name made lowercase.
    job_address = models.ForeignKey(JobCitys, models.DO_NOTHING, db_column='job_address', blank=True, null=True)
    job_jy = models.CharField(max_length=100, blank=True, null=True)
    job_xl = models.CharField(max_length=100, blank=True, null=True)
    job_hrname = models.CharField(db_column='job_hrName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    job_hrleader = models.CharField(max_length=100, blank=True, null=True)
    job_zwtext = models.TextField(blank=True, null=True)
    job_tdtext = models.TextField(blank=True, null=True)
    job_gstext = models.TextField(blank=True, null=True)
    job_comname = models.CharField(db_column='job_comName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    company_username = models.CharField(db_column='company_userName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    company_money = models.CharField(max_length=100, blank=True, null=True)
    company_time = models.CharField(max_length=100, blank=True, null=True)
    company_type = models.CharField(max_length=100, blank=True, null=True)
    company_status = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'job_msg_final'

        verbose_name='岗位信息详情'
        verbose_name_plural=verbose_name


