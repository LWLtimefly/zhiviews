from django.urls import path

from searchapp import views, views_chars

urlpatterns = [
    path('',views.home),
    path('changecity/',views.changecity),
    path('search/',views.search),
    path('charts/', views_chars.index),
    path('xiangxi/<int:id>', views.xiangxi),
    path('search_chart/',views.search_chart),

]
