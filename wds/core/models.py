from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
#from notifications.models import Notification
#from django.dispatch import receiver
# Create your models here.
stock_list = (
    ('RBLBANK', 'RBLBANK'),
    ('MARUTI', 'MARUTI'),
    ('ADANIENT', 'ADANIENT'),
    ('TATASTEEL', 'TATASTEEL'),
    ('BOSCHLTD', 'BOSCHLTD'),
    ('RELIANCE', 'RELIANCE'),
    ('INFOSYS', 'INFOSYS'),
    ('BHARTIARTL', 'BHARTIARTL'),
    ('ITC', 'ITC'),
    ('HDFCBANK', 'HDFCBANK'),
    ('CIPLA', 'CIPLA'),
    ('TCS', 'TCS'),
    ('TATAMOTORS', 'TATAMOTORS'),
    ('ASIANPAINT', 'ASIANPAINT'),
    ('ICICIBANK', 'ICICIBANK'),
    ('HINDUNILVR', 'HINDUNILVR'),
    ('GLENMARK', 'GLENMARK'),
    ('LUPIN', 'LUPIN'),
    ('ONGC', 'ONGC'),
    ('NETWORK18', 'NETWORK18'),
)
status_list = (
    ('accepted', 'accepted'),
    ('declined', 'declined'),
    ('pending', 'pending'),
    ('cancelled', 'cancelled'),
)
action_list = (
    ('buy', 'buy'),
    ('sell', 'sell')
)


class LoggedInUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="logged_in_user", on_delete=models.CASCADE)
    session_key = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.user.username


class StockList(models.Model):
    stockattribute = models.CharField(max_length=20, default="STOCK")
    stockname = models.CharField(max_length=100)
    stockprice = models.FloatField(default=0)

    def __str__(self):
        return f"{self.stockname}"


class Stock(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    userbalance = models.FloatField(default=100000.0)
    RBLBANK = models.IntegerField(default=0)
    MARUTI = models.IntegerField(default=0)
    ADANIENT = models.IntegerField(default=0)
    TATASTEEL = models.IntegerField(default=0)
    BOSCHLTD = models.IntegerField(default=0)
    RELIANCE = models.IntegerField(default=0)
    INFOSYS = models.IntegerField(default=0)
    BHARTIARTL = models.IntegerField(default=0)
    ITC = models.IntegerField(default=0)
    HDFCBANK = models.IntegerField(default=0)
    CIPLA = models.IntegerField(default=0)
    TCS = models.IntegerField(default=0)
    TATAMOTORS = models.IntegerField(default=0)
    ASIANPAINT = models.IntegerField(default=0)
    ICICIBANK = models.IntegerField(default=0)
    HINDUNILVR = models.IntegerField(default=0)
    GLENMARK = models.IntegerField(default=0)
    LUPIN = models.IntegerField(default=0)
    ONGC = models.IntegerField(default=0)
    NETWORK18 = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user}"


class trade(models.Model):
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stock = models.CharField(choices=stock_list, max_length=100)
    numberofstocks = models.IntegerField(default=0)
    priceperstock = models.FloatField(null=True, blank=True, default=0.0)
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='buyer_of_stock', on_delete=models.CASCADE)
    # userbalance=models.FloatField(default=1000000.0)


def create_stock(sender, instance, created, **kwargs):
    if created:
        Stock.objects.create(user=instance)


post_save.connect(create_stock, sender=User)


class tradereq(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender_trade")
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver_trade")
    action = models.CharField(
        choices=action_list, max_length=10, default='buy')
    status = models.CharField(
        choices=status_list, max_length=50, default='pending')
    stock = models.CharField(choices=stock_list, max_length=100)
    numberofstocks = models.IntegerField(default=0)
    priceperstock = models.FloatField(null=True, blank=False, default=0)
    is_active = models.BooleanField(blank=False, null=False, default=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        receiver_stock = Stock.objects.get(user=self.receiver)
        sender_stock = Stock.objects.get(user=self.sender)
        amount = self.numberofstocks*self.priceperstock
        if self.action == 'buy':
            sender_stock.userbalance = sender_stock.userbalance-amount
            receiver_stock.userbalance = receiver_stock.userbalance + \
                (amount*0.97)

            if self.stock == 'RBLBANK':
                if (receiver_stock.RBLBANK >= self.numberofstocks):
                    if(sender_stock.userbalance >= amount):
                        sender_stock.RBLBANK = sender_stock.RBLBANK+self.numberofstocks
                        receiver_stock.RBLBANK = receiver_stock.RBLBANK-self.numberofstocks
                        self.is_active = False
                        self.status = 'accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')

            elif self.stock == 'MARUTI':
                if (receiver_stock.MARUTI >= self.numberofstocks):
                    if(sender_stock.userbalance >= amount):
                        sender_stock.MARUTI = sender_stock.MARUTI+self.numberofstocks
                        receiver_stock.MARUTI = receiver_stock.MARUTI-self.numberofstocks
                        self.is_active = False
                        self.status = 'accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')

            elif self.stock == 'ADANIENT':
                if (receiver_stock.ADANIENT >= self.numberofstocks):
                    if(sender_stock.userbalance >= amount):
                        sender_stock.ADANIENT = sender_stock.ADANIENT+self.numberofstocks
                        receiver_stock.ADANIENT = receiver_stock.ADANIENT-self.numberofstocks
                        self.is_active = False
                        self.status = 'accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock == 'TATASTEEL':
                if (receiver_stock.TATASTEEL >= self.numberofstocks):
                    if(sender_stock.userbalance >= amount):
                        sender_stock.TATASTEEL = sender_stock.TATASTEEL+self.numberofstocks
                        receiver_stock.TATASTEEL = receiver_stock.TATASTEEL-self.numberofstocks
                        self.is_active = False
                        self.status = 'accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')

            elif self.stock == 'BOSCHLTD':
                if (receiver_stock.BOSCHLTD >= self.numberofstocks):
                    if(sender_stock.userbalance >= amount):
                        sender_stock.BOSCHLTD = sender_stock.BOSCHLTD+self.numberofstocks
                        receiver_stock.BOSCHLTD = receiver_stock.BOSCHLTD-self.numberofstocks
                        self.is_active = False
                        self.status = 'accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock == 'RELIANCE':
                if (receiver_stock.RELIANCE >= self.numberofstocks):
                    if(sender_stock.userbalance >= amount):
                        sender_stock.RELIANCE = sender_stock.RELIANCE+self.numberofstocks
                        receiver_stock.RELIANCE = receiver_stock.RELIANCE-self.numberofstocks
                        self.is_active = False
                        self.status = 'accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock == 'INFOSYS':
                if (receiver_stock.INFOSYS >= self.numberofstocks):
                    if(sender_stock.userbalance >= amount):
                        sender_stock.INFOSYS = sender_stock.INFOSYS+self.numberofstocks
                        receiver_stock.INFOSYS = receiver_stock.INFOSYS-self.numberofstocks
                        self.is_active = False
                        self.status = 'accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')

            elif self.stock == 'BHARTIARTL':
                if (receiver_stock.BHARTIARTL >= self.numberofstocks):
                    if(sender_stock.userbalance >= amount):
                        sender_stock.BHARTIARTL = sender_stock.BHARTIARTL+self.numberofstocks
                        receiver_stock.BHARTIARTL = receiver_stock.BHARTIARTL-self.numberofstocks
                        self.is_active = False
                        self.status = 'accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')

            elif self.stock == 'ITC':
                if (receiver_stock.ITC >= self.numberofstocks):
                    if(sender_stock.userbalance >= amount):
                        sender_stock.ITC = sender_stock.ITC+self.numberofstocks
                        receiver_stock.ITC = receiver_stock.ITC-self.numberofstocks
                        self.is_active = False
                        self.status = 'accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock == 'HDFCBANK':
                if (receiver_stock.HDFCBANK >= self.numberofstocks):
                    if(sender_stock.userbalance >= amount):
                        sender_stock.HDFCBANK = sender_stock.HDFCBANK+self.numberofstocks
                        receiver_stock.HDFCBANK = receiver_stock.HDFCBANK-self.numberofstocks
                        self.is_active = False
                        self.status = 'accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')

            elif self.stock == 'CIPLA':
                if (receiver_stock.CIPLA >= self.numberofstocks):
                    if(sender_stock.userbalance >= amount):
                        sender_stock.CIPLA = sender_stock.CIPLA+self.numberofstocks
                        receiver_stock.CIPLA = receiver_stock.CIPLA-self.numberofstocks
                        self.is_active = False
                        self.status = 'accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock == 'TCS':
                if (receiver_stock.TCS >= self.numberofstocks):
                    if(sender_stock.userbalance >= amount):
                        sender_stock.TCS = sender_stock.TCS+self.numberofstocks
                        receiver_stock.TCS = receiver_stock.TCS-self.numberofstocks
                        self.is_active = False
                        self.status = 'accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock == 'TATAMOTORS':
                if (receiver_stock.TATAMOTORS >= self.numberofstocks):
                    if(sender_stock.userbalance >= amount):
                        sender_stock.TATAMOTORS = sender_stock.TATAMOTORS+self.numberofstocks
                        receiver_stock.TATAMOTORS = receiver_stock.TATAMOTORS-self.numberofstocks
                        self.is_active = False
                        self.status = 'accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock == 'ASIANPAINT':
                if (receiver_stock.ASIANPAINT >= self.numberofstocks):
                    if(sender_stock.userbalance >= amount):
                        sender_stock.ASIANPAINT = sender_stock.ASIANPAINT+self.numberofstocks
                        receiver_stock.ASIANPAINT = receiver_stock.ASIANPAINT-self.numberofstocks
                        self.is_active = False
                        self.status = 'accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock == 'ICICIBANK':
                if (receiver_stock.ICICIBANK >= self.numberofstocks):
                    if(sender_stock.userbalance >= amount):
                        sender_stock.ICICIBANK = sender_stock.ICICIBANK+self.numberofstocks
                        receiver_stock.ICICIBANK = receiver_stock.ICICIBANK-self.numberofstocks
                        self.is_active = False
                        self.status = 'accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock == 'HINDUNILVR':
                if (receiver_stock.HINDUNILVR >= self.numberofstocks):
                    if(sender_stock.userbalance >= amount):
                        sender_stock.HINDUNILVR = sender_stock.HINDUNILVR+self.numberofstocks
                        receiver_stock.HINDUNILVR = receiver_stock.HINDUNILVR-self.numberofstocks
                        self.is_active = False
                        self.status = 'accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock == 'GLENMARK':
                if (receiver_stock.GLENMARK >= self.numberofstocks):
                    if(sender_stock.userbalance >= amount):
                        sender_stock.GLENMARK = sender_stock.GLENMARK+self.numberofstocks
                        receiver_stock.GLENMARK = receiver_stock.GLENMARK-self.numberofstocks
                        self.is_active = False
                        self.status = 'accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock == 'ONGC':
                if (receiver_stock.ONGC >= self.numberofstocks):
                    if(sender_stock.userbalance >= amount):
                        sender_stock.ONGC = sender_stock.ONGC+self.numberofstocks
                        receiver_stock.ONGC = receiver_stock.ONGC-self.numberofstocks
                        self.is_active = False
                        self.status = 'accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock == 'LUPIN':
                if (receiver_stock.LUPIN >= self.numberofstocks):
                    if(sender_stock.userbalance >= amount):
                        sender_stock.LUPIN = sender_stock.LUPIN+self.numberofstocks
                        receiver_stock.LUPIN = receiver_stock.LUPIN-self.numberofstocks
                        self.is_active = False
                        self.status = 'accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')
            elif self.stock == 'NETWORK18':
                if (receiver_stock.NETWORK18 >= self.numberofstocks):
                    if(sender_stock.userbalance >= amount):
                        sender_stock.NETWORK18 = sender_stock.NETWORK18+self.numberofstocks
                        receiver_stock.NETWORK18 = receiver_stock.NETWORK18-self.numberofstocks
                        self.is_active = False
                        self.status = 'accepted'
                    else:
                        return ('Currently Sender have Insufficient Balance to Buy!')
                else:
                    return ('Insufficient Stock Holdings')



            receiver_stock.save()
            sender_stock.save()
        elif self.action == 'sell':
            sender_stock, receiver_stock = receiver_stock, sender_stock
            if (amount <= sender_stock.userbalance):
                sender_stock.userbalance = sender_stock.userbalance-amount
                receiver_stock.userbalance = receiver_stock.userbalance + \
                    (amount*0.97)
                if self.stock == 'RBLBANK':
                    if(receiver_stock.RBLBANK >= self.numberofstocks):
                        sender_stock.RBLBANK = sender_stock.RBLBANK+self.numberofstocks
                        receiver_stock.RBLBANK = receiver_stock.RBLBANK-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock == 'MARUTI':
                    if(receiver_stock.MARUTI >= self.numberofstocks):
                        sender_stock.MARUTI = sender_stock.MARUTI+self.numberofstocks
                        receiver_stock.MARUTI = receiver_stock.MARUTI-self.numberofstocks
                    else:
                        print('Current Stocks insufficient')
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock == 'ADANIENT':
                    if(receiver_stock.ADANIENT >= self.numberofstocks):
                        sender_stock.ADANIENT = sender_stock.ADANIENT+self.numberofstocks
                        receiver_stock.ADANIENT = receiver_stock.ADANIENT-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock == 'TATASTEEL':
                    if(receiver_stock.TATASTEEL >= self.numberofstocks):
                        sender_stock.TATASTEEL = sender_stock.TATASTEEL+self.numberofstocks
                        receiver_stock.TATASTEEL = receiver_stock.TATASTEEL-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock == 'BOSCHLTD':
                    if(receiver_stock.BOSCHLTD >= self.numberofstocks):
                        sender_stock.BOSCHLTD = sender_stock.BOSCHLTD+self.numberofstocks
                        receiver_stock.BOSCHLTD = receiver_stock.BOSCHLTD-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock == 'RELIANCE':
                    if(receiver_stock.RELIANCE >= self.numberofstocks):
                        sender_stock.RELIANCE = sender_stock.RELIANCE+self.numberofstocks
                        receiver_stock.RELIANCE = receiver_stock.RELIANCE-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock == 'INFOSYS':
                    if(receiver_stock.INFOSYS >= self.numberofstocks):
                        sender_stock.INFOSYS = sender_stock.INFOSYS+self.numberofstocks
                        receiver_stock.INFOSYS = receiver_stock.INFOSYS-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock == 'BHARTIARTL':
                    if(receiver_stock.BHARTIARTL >= self.numberofstocks):
                        sender_stock.BHARTIARTL = sender_stock.BHARTIARTL+self.numberofstocks
                        receiver_stock.BHARTIARTL = receiver_stock.BHARTIARTL-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock == 'ITC':
                    if(receiver_stock.ITC >= self.numberofstocks):
                        sender_stock.ITC = sender_stock.ITC+self.numberofstocks
                        receiver_stock.ITC = receiver_stock.ITC-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock == 'HDFCBANK':
                    if(receiver_stock.HDFCBANK >= self.numberofstocks):
                        sender_stock.HDFCBANK = sender_stock.HDFCBANK+self.numberofstocks
                        receiver_stock.HDFCBANK = receiver_stock.HDFCBANK-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock == 'CIPLA':
                    if(receiver_stock.CIPLA >= self.numberofstocks):
                        sender_stock.CIPLA = sender_stock.CIPLA+self.numberofstocks
                        receiver_stock.CIPLA = receiver_stock.CIPLA-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock == 'TCS':
                    if(receiver_stock.TCS >= self.numberofstocks):
                        sender_stock.TCS = sender_stock.TCS+self.numberofstocks
                        receiver_stock.TCS = receiver_stock.TCS-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock == 'TATAMOTORS':
                    if(receiver_stock.TATAMOTORS >= self.numberofstocks):
                        sender_stock.TATAMOTORS = sender_stock.TATAMOTORS+self.numberofstocks
                        receiver_stock.TATAMOTORS = receiver_stock.TATAMOTORS-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock == 'ASIANPAINT':
                    if(receiver_stock.ASIANPAINT >= self.numberofstocks):
                        sender_stock.ASIANPAINT = sender_stock.ASIANPAINT+self.numberofstocks
                        receiver_stock.ASIANPAINT = receiver_stock.ASIANPAINT-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock == 'ICICIBANK':
                    if(receiver_stock.ICICIBANK >= self.numberofstocks):
                        sender_stock.ICICIBANK = sender_stock.ICICIBANK+self.numberofstocks
                        receiver_stock.ICICIBANK = receiver_stock.ICICIBANK-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock == 'HINDUNILVR':
                    if(receiver_stock.HINDUNILVR >= self.numberofstocks):
                        sender_stock.HINDUNILVR = sender_stock.HINDUNILVR+self.numberofstocks
                        receiver_stock.HINDUNILVR = receiver_stock.HINDUNILVR-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock == 'GLENMARK':
                    if(receiver_stock.GLENMARK >= self.numberofstocks):
                        sender_stock.GLENMARK = sender_stock.GLENMARK+self.numberofstocks
                        receiver_stock.GLENMARK = receiver_stock.GLENMARK-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock == 'LUPIN':
                    if(receiver_stock.LUPIN >= self.numberofstocks):
                        sender_stock.LUPIN = sender_stock.LUPIN+self.numberofstocks
                        receiver_stock.LUPIN = receiver_stock.LUPIN-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock == 'ONGC':
                    if(receiver_stock.ONGC >= self.numberofstocks):
                        sender_stock.ONGC = sender_stock.ONGC+self.numberofstocks
                        receiver_stock.ONGC = receiver_stock.ONGC-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')
                elif self.stock == 'NETWORK18':
                    if(receiver_stock.NETWORK18 >= self.numberofstocks):
                        sender_stock.NETWORK18 = sender_stock.NETWORK18+self.numberofstocks
                        receiver_stock.NETWORK18 = receiver_stock.NETWORK18-self.numberofstocks
                    else:
                        return ('Currently Sender do not have sufficient stocks to sell!')







                self.is_active = False
                self.status = 'accepted'
            else:
                return ('Insufficient Balance')

            receiver_stock.save()
            sender_stock.save()
        # self.is_active=False
        # self.status="accepted"
        print(self.status)
        trading = trade.objects.create(
            seller=self.receiver,
            stock=self.stock,
            numberofstocks=self.numberofstocks,
            priceperstock=self.priceperstock,
            buyer=self.sender,
            # userbalance=userbalance,
        )
        self.save()

    def decline(self):
        self.is_active = False
        self.status = "declined"
        print(self.status)
        self.save()

    def cancel(self):
        self.is_active = False
        self.status = "cancelled"
        print(self.status)
        self.save()


class Report(models.Model):
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reporter")
    reporting = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.reporter}"
