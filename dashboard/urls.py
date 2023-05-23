# 全てのページにアクセス（ログイン画面などは除く）
from django.urls import path
from . import views

from django.contrib.staticfiles.urls import staticfiles_urlpatterns #stream
from django.conf.urls.static import static      #stream


urlpatterns = [
    path('dashboard/',views.index,name="dashboard-index"),
    
    path('staff/',views.staff,name='dashboard-staff'),
    path('staff/detail/<int:pk>/',views.staff_detail,name='dashboard-staff-detail'),

    path('product/',views.product,name='dashboard-product'),
    path('product/delete/<int:pk>/',views.product_delete,name='dashboard-product-delete'),
    path('product/update/<int:pk>/',views.product_update,name='dashboard-product-update'),

    path('home/',views.home,name='dashboard-home'),

    path('stream/', views.IndexView.as_view(),name="dashboard-stream"), #st
    path('video_feed/', views.video_feed_view(), name="video_feed"), #st
    path('video_feed2/', views.video_feed_view2(), name="video_feed2"),

    path('answer/',views.answer,name="dashboard-answer"),
    
    path('month/',views.monthdata,name='dashboard-month'),
    path('date/',views.date,name="dashboard-date"),
    path('apple/<int:pk>/',views.apple,name="dashboard-apple"),
]
urlpatterns += staticfiles_urlpatterns()