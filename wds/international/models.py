from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
#from notifications.models import Notification
#from django.dispatch import receiver
# Create your models here.
stock_list=(
    ('JPM','JPM'),
    ('ATT','ATT'),
    ('NFLX','NFLX'),
    ('AMZN','AMZN'),
    ('PFE','PFE'),
    ('MRNA','MRNA'),
    ('NKE','NKE'),
    ('META','META'),
    ('ADBE','ADBE'),
    ('PYPL','PYPL'),
    ('BA','BA'),
    ('SBUX','SBUX'),
    ('APL','APL'),
    ('TSLA','TSLA'),
    ('GOOGL','GOOGL'),
    ('TMUS','TMUS'),
    ('GS','GS'),
    ('GM','GM'),
    ('KO','KO'),
    ('TGT','TGT'),
    
)
status_list=(
    ('accepted','accepted'),
    ('declined','declined'),
    ('pending','pending'),
    ('cancelled','cancelled'),
)
action_list=(
    ('buy','buy'),
    ('sell','sell')
)

'''class LoggedInUserInternational(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="logged_in_user_international", on_delete=models.CASCADE)
    session_key = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.user.username
'''
class StockList(models.Model):
    stockattribute = models.CharField(max_length=20)
    stockname = models.CharField(max_length=100)
    stockprice = models.FloatField(default=0)
    def __str__(self):
        return f"{self.stockname}"


class Stock(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,related_name='inter' ,on_delete=models.CASCADE, default=1)
    userbalance=models.FloatField(default=100000.0)
    JPM=models.IntegerField(default=0)
    ATT=models.IntegerField(default=0)
    NFLX=models.IntegerField(default=0)
    AMZN=models.IntegerField(default=0)
    PFE=models.IntegerField(default=0)
    MRNA=models.IntegerField(default=0)
    NKE=models.IntegerField(default=0)
    META=models.IntegerField(default=0)
    ADBE=models.IntegerField(default=0)
    PYPL=models.IntegerField(default=0)
    BA=models.IntegerField(default=0)
    SBUX=models.IntegerField(default=0)
    APL=models.IntegerField(default=0)
    TSLA=models.IntegerField(default=0)
    GOOGL=models.IntegerField(default=0)
    TMUS=models.IntegerField(default=0)
    GS=models.IntegerField(default=0)
    GM=models.IntegerField(default=0)
    KO=models.IntegerField(default=0)
    TGT=models.IntegerField(default=0)
    
    
    def __str__(self):
        return f"{self.user}"
        
class trade(models.Model):
    seller=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='seller_of_stock_international',on_delete=models.CASCADE)
    stock=models.CharField(choices=stock_list,max_length=100)
    numberofstocks=models.IntegerField(default=0)
    priceperstock=models.FloatField(null=True, blank=True)
    buyer=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='buyer_of_stock_international', on_delete=models.CASCADE)
    #userbalance=models.FloatField(default=1000000.0)
    

def create_stock(sender,instance,created,**kwargs):
    if created:
        Stock.objects.create(user=instance)

post_save.connect(create_stock,sender=User)



class tradereq(models.Model):
    sender=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender_trade_inter")
    receiver=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver_trade_inter")
    action=models.CharField(choices=action_list,max_length=10,default='buy')
    status=models.CharField(choices=status_list,max_length=50,default='pending')
    stock=models.CharField(choices=stock_list,max_length=100)
    numberofstocks=models.IntegerField(default=0)
    priceperstock=models.FloatField(null=True, blank=False, default=0)
    is_active= models.BooleanField(blank=False, null=False, default=True)
    
    def __str__(self):
        return self.sender.username
    def accept(self):
        receiver_stock=Stock.objects.get(user=self.receiver)
        sender_stock=Stock.objects.get(user=self.sender)
        amount=self.numberofstocks*self.priceperstock
        if self.action=='buy':
            sender_stock.userbalance=sender_stock.userbalance-amount
            receiver_stock.userbalance=receiver_stock.userbalance+(amount*0.97)
            if self.stock=='JPM':
                if (receiver_stock.JPM>=self.numberofstocks):
                    if(sender_stock.userbalance>=amount):
                        sender_stock.JPM=sender_stock.JPM+self.numberofstocks
                        receiver_stock.JPM=receiver_stock.JPM-self.numberofstocks
                        self.is_active=False
                        self.status='accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock=='ATT':
                if (receiver_stock.ATT>=self.numberofstocks):
                    if(sender_stock.userbalance>=amount):
                        sender_stock.ATT=sender_stock.ATT+self.numberofstocks
                        receiver_stock.ATT=receiver_stock.ATT-self.numberofstocks
                        self.is_active=False
                        self.status='accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock=='NFLX':
                if (receiver_stock.NFLX>=self.numberofstocks):
                    if(sender_stock.userbalance>=amount):
                        sender_stock.NFLX=sender_stock.NFLX+self.numberofstocks
                        receiver_stock.NFLX=receiver_stock.NFLX-self.numberofstocks
                        self.is_active=False
                        self.status='accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock=='AMZN':
                if (receiver_stock.AMZN>=self.numberofstocks):
                    if(sender_stock.userbalance>=amount):
                        sender_stock.AMZN=sender_stock.AMZN+self.numberofstocks
                        receiver_stock.AMZN=receiver_stock.AMZN-self.numberofstocks
                        self.is_active=False
                        self.status='accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            
            elif self.stock=='PFE':
                if (receiver_stock.PFE>=self.numberofstocks):
                    if(sender_stock.userbalance>=amount):
                        sender_stock.PFE=sender_stock.PFE+self.numberofstocks
                        receiver_stock.PFE=receiver_stock.PFE-self.numberofstocks
                        self.is_active=False
                        self.status='accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock=='MRNA':
                if (receiver_stock.MRNA>=self.numberofstocks):
                    if(sender_stock.userbalance>=amount):
                        sender_stock.MRNA=sender_stock.MRNA+self.numberofstocks
                        receiver_stock.MRNA=receiver_stock.MRNA-self.numberofstocks
                        self.is_active=False
                        self.status='accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock=='NKE':
                if (receiver_stock.NKE>=self.numberofstocks):
                    if(sender_stock.userbalance>=amount):
                        sender_stock.NKE=sender_stock.NKE+self.numberofstocks
                        receiver_stock.NKE=receiver_stock.NKE-self.numberofstocks
                        self.is_active=False
                        self.status='accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock=='META':
                if (receiver_stock.META>=self.numberofstocks):
                    if(sender_stock.userbalance>=amount):
                        sender_stock.META=sender_stock.META+self.numberofstocks
                        receiver_stock.META=receiver_stock.META-self.numberofstocks
                        self.is_active=False
                        self.status='accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            
            elif self.stock=='ADBE':
                if (receiver_stock.ADBE>=self.numberofstocks):
                    if(sender_stock.userbalance>=amount):
                        sender_stock.ADBE=sender_stock.ADBE+self.numberofstocks
                        receiver_stock.ADBE=receiver_stock.ADBE-self.numberofstocks
                        self.is_active=False
                        self.status='accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock=='PYPL':
                if (receiver_stock.PYPL>=self.numberofstocks):
                    if(sender_stock.userbalance>=amount):
                        sender_stock.PYPL=sender_stock.PYPL+self.numberofstocks
                        receiver_stock.PYPL=receiver_stock.PYPL-self.numberofstocks
                        self.is_active=False
                        self.status='accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock=='BA':
                if (receiver_stock.BA>=self.numberofstocks):
                    if(sender_stock.userbalance>=amount):
                        sender_stock.BA=sender_stock.BA+self.numberofstocks
                        receiver_stock.BA=receiver_stock.BA-self.numberofstocks
                        self.is_active=False
                        self.status='accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock=='SBUX':
                if (receiver_stock.SBUX>=self.numberofstocks):
                    if(sender_stock.userbalance>=amount):
                        sender_stock.SBUX=sender_stock.SBUX+self.numberofstocks
                        receiver_stock.SBUX=receiver_stock.SBUX-self.numberofstocks
                        self.is_active=False
                        self.status='accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock=='APL':
                if (receiver_stock.APL>=self.numberofstocks):
                    if(sender_stock.userbalance>=amount):
                        sender_stock.APL=sender_stock.APL+self.numberofstocks
                        receiver_stock.APL=receiver_stock.APL-self.numberofstocks
                        self.is_active=False
                        self.status='accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock=='TSLA':
                if (receiver_stock.TSLA>=self.numberofstocks):
                    if(sender_stock.userbalance>=amount):
                        sender_stock.TSLA=sender_stock.TSLA+self.numberofstocks
                        receiver_stock.TSLA=receiver_stock.TSLA-self.numberofstocks
                        self.is_active=False
                        self.status='accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock=='GOOGL':
                if (receiver_stock.GOOGL>=self.numberofstocks):
                    if(sender_stock.userbalance>=amount):
                        sender_stock.GOOGL=sender_stock.GOOGL+self.numberofstocks
                        receiver_stock.GOOGL=receiver_stock.GOOGL-self.numberofstocks
                        self.is_active=False
                        self.status='accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock=='TMUS':
                if (receiver_stock.TMUS>=self.numberofstocks):
                    if(sender_stock.userbalance>=amount):
                        sender_stock.TMUS=sender_stock.TMUS+self.numberofstocks
                        receiver_stock.TMUS=receiver_stock.TMUS-self.numberofstocks
                        self.is_active=False
                        self.status='accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock=='GS':
                if (receiver_stock.GS>=self.numberofstocks):
                    if(sender_stock.userbalance>=amount):
                        sender_stock.GS=sender_stock.GS+self.numberofstocks
                        receiver_stock.GS=receiver_stock.GS-self.numberofstocks
                        self.is_active=False
                        self.status='accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock=='GM':
                if (receiver_stock.GM>=self.numberofstocks):
                    if(sender_stock.userbalance>=amount):
                        sender_stock.GM=sender_stock.GM+self.numberofstocks
                        receiver_stock.GM=receiver_stock.GM-self.numberofstocks
                        self.is_active=False
                        self.status='accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock=='KO':
                if (receiver_stock.KO>=self.numberofstocks):
                    if(sender_stock.userbalance>=amount):
                        sender_stock.KO=sender_stock.KO+self.numberofstocks
                        receiver_stock.KO=receiver_stock.KO-self.numberofstocks
                        self.is_active=False
                        self.status='accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock=='TGT':
                if (receiver_stock.TGT>=self.numberofstocks):
                    if(sender_stock.userbalance>=amount):
                        sender_stock.TGT=sender_stock.TGT+self.numberofstocks
                        receiver_stock.TGT=receiver_stock.TGT-self.numberofstocks
                        self.is_active=False
                        self.status='accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            



            
            receiver_stock.save()
            sender_stock.save()
        elif self.action=='sell':
            sender_stock,receiver_stock=receiver_stock,sender_stock
            if (amount<=sender_stock.userbalance):
                
                sender_stock.userbalance=sender_stock.userbalance-amount
                receiver_stock.userbalance=receiver_stock.userbalance+(amount*0.97)
                if self.stock=='JPM':
                    if(receiver_stock.JPM>=self.numberofstocks):
                        sender_stock.JPM=sender_stock.JPM+self.numberofstocks
                        receiver_stock.JPM=receiver_stock.JPM-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock=='ATT':
                    if(receiver_stock.ATT>=self.numberofstocks):
                        sender_stock.ATT=sender_stock.ATT+self.numberofstocks
                        receiver_stock.ATT=receiver_stock.ATT-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock=='NFLX':
                    if(receiver_stock.NFLX>=self.numberofstocks):
                        sender_stock.NFLX=sender_stock.NFLX+self.numberofstocks
                        receiver_stock.NFLX=receiver_stock.NFLX-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock=='AMZN':
                    if(receiver_stock.AMZN>=self.numberofstocks):
                        sender_stock.AMZN=sender_stock.AMZN+self.numberofstocks
                        receiver_stock.AMZN=receiver_stock.AMZN-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock=='PFE':
                    if(receiver_stock.PFE>=self.numberofstocks):
                        sender_stock.PFE=sender_stock.PFE+self.numberofstocks
                        receiver_stock.PFE=receiver_stock.PFE-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock=='MRNA':
                    if(receiver_stock.MRNA>=self.numberofstocks):
                        sender_stock.MRNA=sender_stock.MRNA+self.numberofstocks
                        receiver_stock.MRNA=receiver_stock.MRNA-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock=='NKE':
                    if(receiver_stock.NKE>=self.numberofstocks):
                        sender_stock.NKE=sender_stock.NKE+self.numberofstocks
                        receiver_stock.NKE=receiver_stock.NKE-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock=='META':
                    if(receiver_stock.META>=self.numberofstocks):
                        sender_stock.META=sender_stock.META+self.numberofstocks
                        receiver_stock.META=receiver_stock.META-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock=='ADBE':
                    if(receiver_stock.ADBE>=self.numberofstocks):
                        sender_stock.ADBE=sender_stock.ADBE+self.numberofstocks
                        receiver_stock.ADBE=receiver_stock.ADBE-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock=='PYPL':
                    if(receiver_stock.PYPL>=self.numberofstocks):
                        sender_stock.PYPL=sender_stock.PYPL+self.numberofstocks
                        receiver_stock.PYPL=receiver_stock.PYPL-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock=='BA':
                    if(receiver_stock.BA>=self.numberofstocks):
                        sender_stock.BA=sender_stock.BA+self.numberofstocks
                        receiver_stock.BA=receiver_stock.BA-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock=='SBUX':
                    if(receiver_stock.SBUX>=self.numberofstocks):
                        sender_stock.SBUX=sender_stock.SBUX+self.numberofstocks
                        receiver_stock.SBUX=receiver_stock.SBUX-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock=='APL':
                    if(receiver_stock.APL>=self.numberofstocks):
                        sender_stock.APL=sender_stock.APL+self.numberofstocks
                        receiver_stock.APL=receiver_stock.APL-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock=='TSLA':
                    if(receiver_stock.TSLA>=self.numberofstocks):
                        sender_stock.TSLA=sender_stock.TSLA+self.numberofstocks
                        receiver_stock.TSLA=receiver_stock.TSLA-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock=='GOOGL':
                    if(receiver_stock.GOOGL>=self.numberofstocks):
                        sender_stock.GOOGL=sender_stock.GOOGL+self.numberofstocks
                        receiver_stock.GOOGL=receiver_stock.GOOGL-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock=='TMUS':
                    if(receiver_stock.TMUS>=self.numberofstocks):
                        sender_stock.TMUS=sender_stock.TMUS+self.numberofstocks
                        receiver_stock.TMUS=receiver_stock.TMUS-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock=='GS':
                    if(receiver_stock.GS>=self.numberofstocks):
                        sender_stock.GS=sender_stock.GS+self.numberofstocks
                        receiver_stock.GS=receiver_stock.GS-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock=='GM':
                    if(receiver_stock.GM>=self.numberofstocks):
                        sender_stock.GM=sender_stock.GM+self.numberofstocks
                        receiver_stock.GM=receiver_stock.GM-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock=='KO':
                    if(receiver_stock.KO>=self.numberofstocks):
                        sender_stock.KO=sender_stock.KO+self.numberofstocks
                        receiver_stock.KO=receiver_stock.KO-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock=='TGT':
                    if(receiver_stock.TGT>=self.numberofstocks):
                        sender_stock.TGT=sender_stock.TGT+self.numberofstocks
                        receiver_stock.TGT=receiver_stock.TGT-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')


                self.is_active=False
                self.status='accepted'
            else:
                return ('Insufficient Balance')


                
            receiver_stock.save()
            sender_stock.save()
        #self.is_active=False
        #self.status="accepted"
        print(self.status)
        trading=trade.objects.create(
                    seller=self.receiver,
                    stock=self.stock,
                    numberofstocks=self.numberofstocks,
                    priceperstock=self.priceperstock,
                    buyer=self.sender,
                    #userbalance=userbalance,
                )
        self.save()
    def decline(self):
        self.is_active=False
        self.status="declined"
        print(self.status)
        self.save()

    def cancel(self):
        self.is_active=False
        self.status="cancelled"
        print(self.status)
        self.save()

class Report(models.Model):
    reporter=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reporter_inter")
    reporting=models.CharField(max_length=100)

    def __str__(self):
        return f"{self.reporter}"