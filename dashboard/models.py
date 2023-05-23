# データベース作成

from django.db import models
#from django.contrib.auth.models import User

# data of judgiment
class Product(models.Model):
    name = models.CharField(max_length=100,null=True)
    quantity = models.PositiveBigIntegerField(null=True)

    thresh = models.PositiveIntegerField(null=True)
    width = models.DecimalField(null=True,max_digits=6,decimal_places=3)
    height = models.DecimalField(null=True,max_digits=6,decimal_places=3)
    class Meta:
        verbose_name_plural = 'Product'
    def __str__(self):
        return f'{self.name}--{self.quantity}--'


# data for calendar
class CalendarYear(models.Model):
    year  = models.CharField(max_length=5)
    class Meta:
        verbose_name_plural = 'CalendarYear'
    def __str__(self):
        return F'Year:{self.year}'

class CalendarMonth(models.Model):
    year = models.ForeignKey(CalendarYear,models.CASCADE, null=True)
    month = models.CharField(max_length=4)
    class Meta:
        verbose_name_plural = 'CalendarMonth'
    def __str__(self):
        return F'Year:{self.year.year}/{self.month}/--'

class Calendarday(models.Model):
    month = models.ForeignKey(CalendarMonth,models.CASCADE, null=True)
    day = models.CharField(max_length=4)
    total = models.PositiveIntegerField(null=True)
    class Meta:
        verbose_name_plural = 'CalendarDay'
    def __str__(self):
        return F'{self.month.year.year}/{self.month.month}/{self.day}'



# data for web
class Answer(models.Model):
    name = models.CharField(max_length=10)
    date = models.TimeField()
    class Meta:
        verbose_name_plural = 'answer'
    def __str__(self):
        return F'{self.name} --- {self.date}'

# date for item conected date
class Item(models.Model):
    date = models.ForeignKey(Calendarday,models.CASCADE, null=True)
    name = models.CharField(max_length=15,null=True)
    quan = models.PositiveIntegerField(null=True)
    
    quan_a = models.PositiveIntegerField(null=True)
    quan_b = models.PositiveIntegerField(null=True)
    quan_c = models.PositiveIntegerField(null=True)
    class Meta:
        verbose_name_plural = 'Item'
    def __str__(self):
        return F'{self.id}-{self.date.day}--{self.name}'