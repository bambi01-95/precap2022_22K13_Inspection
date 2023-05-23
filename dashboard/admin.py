# admin/ のデータベース表示を変える
from tabnanny import verbose
from django.contrib import admin
from .models import Product,Answer,Item,Calendarday,CalendarMonth,CalendarYear
from django.contrib.auth.models import Group #admin site's group
admin.site.site_header = 'DX4F'


# Register your models here.
admin.site.register(Product)
admin.site.register(Answer)
admin.site.register(Item)
admin.site.register(CalendarYear)
admin.site.register(CalendarMonth)
admin.site.register(Calendarday)