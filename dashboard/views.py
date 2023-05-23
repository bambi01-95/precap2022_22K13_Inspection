# ページに移すデータの管理やストリーミング

from django.shortcuts import render,redirect
from django.http import HttpResponse
# import maked something
from django.contrib.auth.decorators import login_required
from .forms import ProductForm

from django.contrib.auth.models import User
from django.contrib import messages

# improt data models
from .models import Product,Answer,Item

# import for js
import random
import datetime
import json # https://teratail.com/questions/299286
from django.http.response import JsonResponse
from .models import Calendarday,CalendarMonth,CalendarYear

# import image proccesing
import sys
import numpy as np
import copy
import cv2
from django.http import StreamingHttpResponse
from django.views import View

import calendar as cal
import time


import socket

#from .judge import predict
@login_required
def index(request):
    products = Product.objects.all()
    context = {
        'products':products,
    }
    return render(request, 'dashboard/index.html',context)



@login_required
def staff(request):#staff/
    workers = User.objects.all()
    context = {
        'workers':workers,
    }
    return render(request, 'dashboard/staff.html',context)

@login_required
def staff_detail(request, pk):#staff/detail/<int:pk>/
    workers = User.objects.get(id=pk)
    context = {
        'workers':workers,

    }
    return render(request,'dashboard/staff_detail.html',context)

@login_required
def product(request):#product/
    items =  Product.objects.all()
    workers = User.objects.all()
    if request.method=='POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            messages.success(request, f'{product_name} has been added')

            return redirect('dashboard-product')
    else:
        form = ProductForm()
    context = {
        'items' : items,
        'form':form,
        'workers':workers,
    }
    return render(request, 'dashboard/product.html',context)

@login_required
def product_delete(request,pk):#product/delete/<int:pk>/
    workers = User.objects.all()
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('dashboard-product')
    return render(request, 'dashboard/product_delete.html')


@login_required
def product_update(request,pk):#product/update/<int:pk>/
    workers = User.objects.all()
    item = Product.objects.get(id=pk)
    if request.method=='POST':
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')
    else:
        form = ProductForm(instance=item)

    context = {
        'form':form,
    }
    return render(request,'dashboard/product_update.html',context)







# home画面　カレンダーで見れる
@login_required
def home(request):#home/ ログインページ
    today = datetime.datetime.now()
    workers = User.objects.all()
        
    if request.method=='POST':
        selectyear = int(request.POST['year'])
        selectmonth = int(request.POST['month'])

    else:
        selectyear  = today.year
        selectmonth = today.month

    print(selectyear)
    print(selectmonth)
    youbi = datetime.date(selectyear,selectmonth,1).weekday()
    years = CalendarYear.objects.all()
    box = np.array([np.arange(1,42,1) - youbi - 1,np.arange(-42,-1,1)]).T
    grahp = {}
    for year in years:
        if(str(year.year)==str(selectyear)):
            for month in year.calendarmonth_set.all():
                if (str(selectmonth)==str(month.month)):
                    grahp = month
                    for day in month.calendarday_set.all():
                        box[int(day.day) + int(youbi) ][1] = day.id
    lastday = cal.monthrange(int(selectyear),int(selectmonth))[1]

    if (selectmonth+1==13):
        nextm = 1
        nexty = selectyear + 1
    else:
        nextm = selectmonth+1
        nexty = selectyear
    if(selectmonth-1)==0:
        previousm = 12
        previousy = selectyear - 1
    else:
        previousm = selectmonth - 1
        previousy = selectyear

    
    data = {
        'grahp':grahp,
        'lastday':lastday,
        'year':selectyear,
        'month':selectmonth,
        'nexty':nexty,
        'nextm':nextm,
        'previousy':previousy,
        'previousm':previousm,
        'today':today,
        'box':box,
        'youbi':youbi+1,
        'workers':workers,#
    }

    return render(request,'dashboard/home.html',data)

# 日付を送信
@login_required
def date(request):# /date のページ
    today = datetime.datetime.now()
    workers = User.objects.all()
    if request.method=='POST':
        selectyear = int(request.POST['year'])
        selectmonth = int(request.POST['month'])

    else:
        selectyear  = today.year
        selectmonth = today.month

    displaymonth = {}
    years = CalendarYear.objects.all()
    for year in years:
        if(str(year.year)==str(selectyear)):
            for month in year.calendarmonth_set.all():
                if (str(selectmonth)==str(month.month)):
                    displaymonth = month

    if (selectmonth+1==13):
        nextm = 1
        nexty = selectyear + 1
    else:
        nextm = selectmonth+1
        nexty = selectyear
    if(selectmonth-1)==0:
        previousm = 12
        previousy = selectyear - 1
    else:
        previousm = selectmonth - 1
        previousy = selectyear

    
    data = {
        'year':selectyear,
        'smonth':selectmonth,

        'nexty':nexty,
        'nextm':nextm,
        'previousy':previousy,
        'previousm':previousm,
        'workers':workers,#
        'month':displaymonth,
    }
    return render(request,'dashboard/date.html',data)

# 日付ごとのデータを送信する
@login_required
def apple(request,pk):#apple/<int:pk>/
    workers = User.objects.all()
    day = Calendarday.objects.get(id=pk)
    content = {
        'day':day,
        'workers':workers,#
    }
    return render(request,'dashboard/apple.html',content)


# 月ごとの製品製造量  /month  
@login_required    
def monthdata(request):
    today = datetime.datetime.now()
    products = Product.objects.all()

    productlist = {}
    for item in products:
        productlist.setdefault(str(item.name),0)
        
    if request.method=='POST':
        selectyear = int(request.POST['year'])
        selectmonth = int(request.POST['month'])
    else:
        selectyear  = today.year
        selectmonth = today.month
    displaymonth = {}
    years = CalendarYear.objects.all()
    
    for year in years:
        if(str(year.year)==str(selectyear)):
            for month in year.calendarmonth_set.all():
                if (str(selectmonth)==str(month.month)):
                    for day in month.calendarday_set.all():
                        for item in day.item_set.all():
                            if (item.name not in productlist):
                                productlist.setdefault(str(item.name),item.quan)
                            else:
                                productlist[item.name] = productlist[item.name] + item.quan
                    break
            break

    items = productlist.items()



    if (selectmonth+1==13):
        nextm = 1
        nexty = selectyear + 1
    else:
        nextm = selectmonth+1
        nexty = selectyear
    if(selectmonth-1)==0:
        previousm = 12
        previousy = selectyear - 1
    else:
        previousm = selectmonth - 1
        previousy = selectyear

    
    data = {
        'items':items,

        'year':selectyear,
        'smonth':selectmonth,

        'nexty':nexty,
        'nextm':nextm,
        'previousy':previousy,
        'previousm':previousm,
        'month':displaymonth,
    }
    return render(request,'dashboard/item.html',data)





# ストリーミング画像・映像を表示するview
# stream/


# 以下のコード全てが　/stream　本体と裏で動作するもの

# 答えデータのリクエストに答える？
@login_required
def answer(request):
    items =  Answer.objects.get(id=1) #using ORM
    dt = datetime.datetime.now()
    h = dt.hour
    m = dt.minute
    s = dt.second
    time = str(h)+":"+str(m)+":"+str(s)
    ans = {
        'name' : items.name,
        'time' : time,
    }
    return JsonResponse(ans)

# id の取得関数
def get_ip():
    host = socket.gethostname()
    # ipアドレスを取得、表示
    mian_ip = socket.gethostbyname(host)
    sub_ip  = mian_ip
    main_port = 8008
    sub_port  = 8080
    return mian_ip,sub_ip,main_port,sub_port

class IndexView(View):
    def get(self, request):
        ip1,ip2,port1,port2 = get_ip()
        address ={
            'ip1':ip1,
            'port1':port1,
        }
        return render(request, 'dashboard/stream.html',address)

# video_feed/
# ストリーミング画像を定期的に返却するview
# 処理されていない動画の出力先
def video_feed_view():
    return lambda _: StreamingHttpResponse(generate_frame(), content_type='multipart/x-mixed-replace; boundary=frame')
# 画像処理後の動画の出力先
def video_feed_view2():
    return lambda _: StreamingHttpResponse(generate_frame2(), content_type='multipart/x-mixed-replace; boundary=frame')

# 画像の受け取る処理を行う
def recive(udp,id):
    buff = 1024 * 64
    while True:
        recive_data = bytes()
            
        while True:
            # 送られてくるデータが大きいので一度に受け取るデータ量を大きく設定
            jpg_str, addr = udp.recvfrom(buff)
            is_len = len(jpg_str) == 7
            is_end = jpg_str == b'__end__'
            if is_len and is_end: 
                break
            recive_data += jpg_str

        jpg_str, addr = udp.recvfrom(buff)
        answer = jpg_str.decode()

        if len(recive_data) == 0: continue
        # string型からnumpyを用いuint8に戻す
        narray = np.fromstring(recive_data, dtype='uint8')

        # uint8のデータを画像データに戻す
        img = cv2.imdecode(narray, 1)

        yield img
        # 画像処理側の動画だった場合、データの更新を行う
        if(id!=-1)&(answer!="__THE__"):
            print("UPDATE START")
            # 在庫の個数データを増やす。
            ari = True
            models = Product.objects.all()
            # データの中に検出物体の名前があるか
            for model in models:
                if(model.name == answer):
                    target_id = model.id
                    ari = False
            if ari:
                return "not data"

            # 検出物体の個数を増やす。
            target = Product.objects.get(id = target_id)
            target.quantity = target.quantity + 1
            target.save()

            # web 出力用のデータを書き換える
            item =  Answer.objects.get(id=1)
            item.name = answer
            item.save()

            # カレンダーの総在庫数を増やす
            date = Calendarday.objects.get(id=id)#id 4///
            date.total = date.total +1
            date.save()

            # 在庫の総量を増やす
            new = True
            for item in date.item_set.all():
                if (item.name==answer):#4;//
                    item.quan = item.quan + 1
                    item.save()
                    new = False
            if (new):# answerで出た答えの物体名がデータになかった際にそれを新たに加える
                newitem = Item(date=date,name=answer,quan=1,quan_a=0,quan_b=0,quan_c=0)
                newitem.save()
            print("UPDATE END")





# フレーム生成・返却する処理 main
def generate_frame():    
    # ipアドレスを取得、表示
    # host = socket.gethostname()
    # ip = socket.gethostbyname(host)
    ip = get_ip()
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # ip port 確認！
    udp.bind((ip, 8008))
    
    # 画像を取り続ける
    for img in recive(udp,-1):
        # フレーム画像バイナリに変換
        ret, jpeg = cv2.imencode('.jpg', img)
        byte_frame = jpeg.tobytes()
        # フレーム画像のバイナリデータをユーザーに送付する
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + byte_frame + b'\r\n\r\n')




# フレーム生成・返却する処理 画像処理後の動画　受信
def generate_frame2():
    start_time = time.time()
    createyear = True
    createmonth = True
    createday = True

    # その日の日付を取得
    today = datetime.datetime.now()      
    selectyear  = today.year
    selectmonth = today.month
    selectday = today.day

    years = CalendarYear.objects.all()
    for year in years:
        if(str(year.year)==str(selectyear)):# データの中に今日の年があるか
            yearid = year
            createyear = False

            for month in year.calendarmonth_set.all():
                if (str(selectmonth)==str(month.month)):# detaの中に今日の月があるか
                    monthid = month
                    createmonth = False

                    for day in month.calendarday_set.all():
                        if(str(selectday) == str(day.day)):# dataの中に今日の日付があるか
                            createday = False
                            dayid = day
                            id = day.id # ある場合、その日のIDを取得
                            break
                    break
            break

    if createyear:# 新しい年のデータを作成
        yearid = CalendarYear(year=selectyear)
        yearid.save()
    
    if createmonth:#　新しい月のデータを作成
        monthid = CalendarMonth(year=yearid,month=selectmonth)
        monthid.save()

    if createday:#　新しい日のデータの作成
        dayid = Calendarday(month=monthid,day=selectday,total=0)
        dayid.save()
        id = dayid.id

    # ipアドレスを取得、表示
    # host = socket.gethostname()
    # ip = socket.gethostbyname(host)
    ip = get_ip()
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind((ip, 8080))

    # 画像を取り続ける
    for img in recive(udp,id):
        # print("get")
        # cv2.imwirte("./get.jpg",img)
        # フレーム画像バイナリに変換
        ret, jpeg = cv2.imencode('.jpg', img)

        byte_frame = jpeg.tobytes()
        # フレーム画像のバイナリデータをユーザーに送付する
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + byte_frame + b'\r\n\r\n')
