from django.contrib import admin
from .models import trade,Stock,tradereq,Report,StockList
# Register your models here.
class stockadmin(admin.ModelAdmin):
    list_display=('user','userbalance','RBLBANK','MARUTI','ADANIENT','TATASTEEL','BOSCHLTD','RELIANCE','INFOSYS','BHARTIARTL','ITC','HDFCBANK','CIPLA','TCS','TATAMOTORS','ASIANPAINT','ICICIBANK','HINDUNILVR','GLENMARK','LUPIN','ONGC','NETWORK18')

class tradeadmin(admin.ModelAdmin):
    list_display=('seller','stock','numberofstocks','priceperstock','buyer')
admin.site.register(Stock,stockadmin)
admin.site.register(trade,tradeadmin)

class requestadmin(admin.ModelAdmin):
    list_display=('sender','receiver','action')
admin.site.register(tradereq,requestadmin)

class reportadmin(admin.ModelAdmin):
    list_display=('reporter','reporting')
admin.site.register(Report,reportadmin)

class stocklistadmin(admin.ModelAdmin):
    list_display=('stockattribute','stockname','stockprice')
admin.site.register(StockList,stocklistadmin)