# import xadmin as admin
# from xadmin import views
#
# from userapp.models import User
#
# # Register your models here.
# class BaseSetting:
#     # 主题修改
#     enable_themes = True
#     use_bootswatch = True
#
#
# class GlobalSettings:
#     # 整体配置
#     site_title = '职友网后台管理平台'
#     site_footer = '娟娟科技'
#     menu_style = 'accordion'  # 菜单折叠
#     # 搜索模型
#     global_search_models = [User]
#
#     # 模型的图标(参考bootstrap图标插件)
#     global_models_icon = {
#         User: "glyphicon glyphicon-book",
#         #JobMsg: "fa fa-cloud"
#     }  # 设置models的全局图标
#
#     #配置应用的名称
#     apps_label_title={
#         'userapp':'user管理'
#     }
#
#     # app_icons={
#     #     ''
#     # }
#
# class UserAdmin:
#     # 后台列表显示列
#     list_display = ['username', 'password','email','phone','image','state','token']
#     # 后台列表查询条件
#     search_fields = ['username']
#
#
# # class JobMsgAdmin:
# #     # 后台列表显示列
# #     list_display = ['job_time', 'job_name', 'job_money', 'job_meanmoney', 'job_address','job_jy','job_xl',
# #                     'job_hrname','job_hrleader','job_zwtext','job_tdtext','job_gstext','job_comname','company_username',
# #                     'company_money','company_time','company_type','company_status']
# #     # 后台列表查询条件
# #     search_fields = ['job_name', 'job_money']
#
#     #设置字段的样式
#     # style_fields={
#     #     'content':'ueditor'
#     # }
#
#
# admin.site.register(views.CommAdminView, GlobalSettings)
# admin.site.register(views.BaseAdminView, BaseSetting)
#
# admin.site.register(User, UserAdmin)
#admin.site.register(JobMsg, JobMsgAdmin)