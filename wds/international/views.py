from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from  django.http import HttpResponse, HttpResponseRedirect
from .forms import RegisterForm,tradeform,requestsellform,tradereqform,reportform
from django.urls import reverse
from .models import Stock,trade,stock_list,tradereq,Report,StockList
import json
from django.db.models import Q
def home(request):
    return render(request,"international/home.html", {'messages': messages.get_messages(request)})

def news(request):
    return render(request,"international/news.html")


def register(request):
    form=RegisterForm()
    if request.method=="POST":
        form=RegisterForm(data=request.POST)

        if (form.is_valid()):
            user=form.save()
            user.set_password(user.password)
            user.save()
            return redirect("/")
        else:
            print(form.errors)
    else:
        form=RegisterForm()
        
    return render(request, 'international/register.html', {'form': form})





def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(username)
        print(password)


        user=authenticate(username=username,password=password)

        if user is not None:
                login(request,user)
        else:
            print("false login")
            messages.error(request, f'Invalid Teamname or Password')
            return redirect('international:userlogin')
        return redirect('/')
    else:
        print("render part ran successfully")
        return render(request,'international/userlogin.html')

@login_required
def userlogout(request):
    print("logout")
    logout(request)
    return redirect('/')

@login_required
def dashboard(request):
    user_dashdata = Stock.objects.filter(user=request.user)
    dash_dic = {'dashdata':user_dashdata}
    return render(request,'international/dashboard.html', {'dashdata':user_dashdata})

def stock_display(request):
    context = {
      'posts': StockList.objects.all()
    }
    return render(request,'international/stocks.html', context)


class Trade(ListView):
    def get(self, *args, **kwargs):
        form = tradeform()
        context = {
            'form':form,
        }
        return render(self.request, 'international/buy-sell-form.html', context)

    def post(self, *args, **kwargs):
        form = tradeform(self.request.POST or None)
        try:
            if form.is_valid():
                seller=form.cleaned_data.get('seller')
                stock=form.cleaned_data.get('stock')
                numberofstocks=form.cleaned_data.get('numberofstocks')
                priceperstock=form.cleaned_data.get('priceperstock')
               # userbalance=form.cleaned_data.get('userbalance')
                buyer=form.cleaned_data.get('buyer')
                trading=trade.objects.create(
                    seller=seller,
                    stock=stock,
                    numberofstocks=numberofstocks,
                    priceperstock=priceperstock,
                    buyer=buyer,
                    #userbalance=userbalance,
                )
                print(priceperstock)
                print(numberofstocks)
                stock_seller=Stock.objects.get(user=seller)
                print(stock_seller)
                          
                stock_buyer=Stock.objects.get(user=buyer)
                print(stock_buyer)
                '''for st in stock_list:
                    if stock==st[0]:
                        stock_seller.st[0]-=numberofstocks
                        stock_seller.userbalance+=priceperstock*numberofstocks
                        stock_buyer.st[0]+=numberofstocks
                        stock_buyer.userbalance-=priceperstock*numberofstocks
                        stock_seller.save()
                        stock_buyer.save()'''

                if stock=="JPM":
                    stock_seller.JPM-=numberofstocks
                    stock_seller.userbalance+=priceperstock*numberofstocks
                    stock_buyer.JPM+=numberofstocks
                    stock_buyer.userbalance-=priceperstock*numberofstocks
                    stock_seller.save()                 
                    stock_buyer.save()
                elif stock=="ATT":
                    stock_seller.ATT-=numberofstocks
                    stock_seller.userbalance+=priceperstock*numberofstocks
                    stock_buyer.ATT+=numberofstocks
                    stock_buyer.userbalance-=priceperstock*numberofstocks
                    stock_seller.save()         
                    stock_seller.save()
                    stock_buyer.save()
                elif stock=="NFLX":
                    stock_seller.NFLX-=numberofstocks
                    stock_seller.userbalance+=priceperstock*numberofstocks
                    stock_buyer.NFLX+=numberofstocks
                    stock_buyer.userbalance-=priceperstock*numberofstocks
                    stock_seller.save()
                    stock_buyer.save()
                elif stock=="AMZN":
                    stock_seller.AMZN-=numberofstocks
                    stock_seller.userbalance+=priceperstock*numberofstocks
                    stock_buyer.AMZN+=numberofstocks
                    stock_buyer.userbalance-=priceperstock*numberofstocks
                    stock_seller.save()
                    stock_buyer.save()
                elif stock=="JPM":
                    stock_seller.JPM-=numberofstocks
                    stock_seller.userbalance+=priceperstock*numberofstocks
                    stock_buyer.JPM+=numberofstocks
                    stock_buyer.userbalance-=priceperstock*numberofstocks
                    stock_seller.save()
                    stock_buyer.save()
                elif stock=="T":
                    stock_seller.T-=numberofstocks
                    stock_seller.userbalance+=priceperstock*numberofstocks
                    stock_buyer.T+=numberofstocks
                    stock_buyer.userbalance-=priceperstock*numberofstocks
                    stock_seller.save()
                    stock_buyer.save()
                elif stock=="PFE":
                    stock_seller.PFE-=numberofstocks
                    stock_seller.userbalance+=priceperstock*numberofstocks
                    stock_buyer.PFE+=numberofstocks
                    stock_buyer.userbalance-=priceperstock*numberofstocks
                    stock_seller.save()
                    stock_buyer.save()
                elif stock=="MRNA":
                    stock_seller.MRNA-=numberofstocks
                    stock_seller.userbalance+=priceperstock*numberofstocks
                    stock_buyer.MRNA+=numberofstocks
                    stock_buyer.userbalance-=priceperstock*numberofstocks
                    stock_seller.save()
                    stock_buyer.save()
                elif stock=="NKE":
                    stock_seller.NKE-=numberofstocks
                    stock_seller.userbalance+=priceperstock*numberofstocks
                    stock_buyer.NKE+=numberofstocks
                    stock_buyer.userbalance-=priceperstock*numberofstocks
                    stock_seller.save()
                    stock_buyer.save()
                elif stock=="META":
                    stock_seller.META-=numberofstocks
                    stock_seller.userbalance+=priceperstock*numberofstocks
                    stock_buyer.META+=numberofstocks
                    stock_buyer.userbalance-=priceperstock*numberofstocks
                    stock_seller.save()
                    stock_buyer.save()
                return redirect('/')
        except ObjectDoesNotExist:
                messages.error(self.request, "fill the form correctly")
                return redirect("/")
@login_required
def reqcreate(request):
    user=request.user
    if request.method=='POST':
        form = tradereqform(request.POST or None)
        if form.is_valid():
                sender=user
                receiver=form.cleaned_data.get('receiver')
                action=form.cleaned_data.get('action')
                stock=form.cleaned_data.get('stock')
                numberofstock=form.cleaned_data.get('numberofstocks')
                priceperstock=form.cleaned_data.get('priceperstock')
                amount = numberofstock*priceperstock
                stock_request_sender=Stock.objects.get(user=sender)
                status='pending'
                #print(StockList.objects.all().values('stockattribute','stockprice').filter(stockattribute=stock).stockprice)
                #print(StockList.objects.all().filter(stockattribute=stock).values('stockprice'))
                markets = StockList.objects.all().filter(stockattribute=stock).values_list('stockprice', flat=True)
                print(markets[0])
                cap = markets[0]*0.1
                lowercap = markets[0]-cap
                uppercap = markets[0]+cap  
                if not (receiver==user):
                    if not (priceperstock<lowercap or priceperstock>uppercap):
                        if action=='buy':
                            if (amount<=stock_request_sender.userbalance):
                                request_trade=tradereq.objects.create(
                                    sender=sender,
                                    receiver=receiver,action=action,
                                    stock=stock,
                                    numberofstocks=numberofstock,
                                    priceperstock=priceperstock,
                                    is_active=True,
                                )
                                return redirect('international:sentreq')
                            else:
                                messages.error(request, f'Insufficient Balance for transaction!!')
                        elif action=='sell':
                            if stock=='JPM':
                                if (numberofstock<=stock_request_sender.JPM):
                                    request_trade=tradereq.objects.create(
                                        sender=sender,
                                        receiver=receiver,action=action,
                                        stock=stock,
                                        numberofstocks=numberofstock,
                                        priceperstock=priceperstock,
                                        is_active=True,
                                    )
                                    return redirect('international:sentreq')
                                else:
                                    messages.error(request, f'Insufficient Stock holdings!!')
                            elif stock=='ATT':
                                if (numberofstock<=stock_request_sender.ATT):
                                    request_trade=tradereq.objects.create(
                                        sender=sender,
                                        receiver=receiver,action=action,
                                        stock=stock,
                                        numberofstocks=numberofstock,
                                        priceperstock=priceperstock,
                                        is_active=True,
                                    )
                                    return redirect('international:sentreq')
                                else:
                                    messages.warning(request, f'Insufficient Stock holdings!!')
                            elif stock=='NFLX':
                                if (numberofstock<=stock_request_sender.NFLX):
                                    request_trade=tradereq.objects.create(
                                        sender=sender,
                                        receiver=receiver,action=action,
                                        stock=stock,
                                        numberofstocks=numberofstock,
                                        priceperstock=priceperstock,
                                        is_active=True,
                                    )
                                    return redirect('international:sentreq')
                                else:
                                    messages.error(request, f'Insufficient Stock holdings!!')
                            elif stock=='AMZN':
                                if (numberofstock<=stock_request_sender.AMZN):
                                    request_trade=tradereq.objects.create(
                                        sender=sender,
                                        receiver=receiver,action=action,
                                        stock=stock,
                                        numberofstocks=numberofstock,
                                        priceperstock=priceperstock,
                                        is_active=True,
                                    )
                                    return redirect('international:sentreq')
                                else:
                                    messages.error(request, f'Insufficient Stock holdings!!')
                            elif stock=='PFE':
                                if (numberofstock<=stock_request_sender.PFE):
                                    request_trade=tradereq.objects.create(
                                        sender=sender,
                                        receiver=receiver,action=action,
                                        stock=stock,
                                        numberofstocks=numberofstock,
                                        priceperstock=priceperstock,
                                        is_active=True,
                                    )
                                    return redirect('international:sentreq')
                                else:
                                    messages.error(request, f'Insufficient Stock holdings!!')
                            elif stock=='MRNA':
                                if (numberofstock<=stock_request_sender.MRNA):
                                    request_trade=tradereq.objects.create(
                                        sender=sender,
                                        receiver=receiver,action=action,
                                        stock=stock,
                                        numberofstocks=numberofstock,
                                        priceperstock=priceperstock,
                                        is_active=True,
                                    )
                                    return redirect('international:sentreq')
                                else:
                                    messages.error(request, f'Insufficient Stock holdings!!')
                            elif stock=='NKE':
                                if (numberofstock<=stock_request_sender.NKE):
                                    request_trade=tradereq.objects.create(
                                        sender=sender,
                                        receiver=receiver,action=action,
                                        stock=stock,
                                        numberofstocks=numberofstock,
                                        priceperstock=priceperstock,
                                        is_active=True,
                                    )
                                    return redirect('international:sentreq')
                                else:
                                    messages.error(request, f'Insufficient Stock holdings!!')
                            elif stock=='META':
                                if (numberofstock<=stock_request_sender.META):
                                    request_trade=tradereq.objects.create(
                                        sender=sender,
                                        receiver=receiver,action=action,
                                        stock=stock,
                                        numberofstocks=numberofstock,
                                        priceperstock=priceperstock,
                                        is_active=True,
                                    )
                                    return redirect('international:sentreq')
                                else:
                                    messages.error(request, f'Insufficient Stock holdings!!')              
                            elif stock=='ADBE':
                                if (numberofstock<=stock_request_sender.ADBE):
                                    request_trade=tradereq.objects.create(
                                        sender=sender,
                                        receiver=receiver,action=action,
                                        stock=stock,
                                        numberofstocks=numberofstock,
                                        priceperstock=priceperstock,
                                        is_active=True,
                                    )
                                    return redirect('international:sentreq')
                                else:
                                    messages.error(request, f'Insufficient Stock holdings!!')
                            elif stock=='PYPL':
                                if (numberofstock<=stock_request_sender.PYPL):
                                    request_trade=tradereq.objects.create(
                                        sender=sender,
                                        receiver=receiver,action=action,
                                        stock=stock,
                                        numberofstocks=numberofstock,
                                        priceperstock=priceperstock,
                                        is_active=True,
                                    )
                                    return redirect('international:sentreq')
                                else:
                                    messages.error(request, f'Insufficient Stock holdings!!')
                            elif stock=='BA':
                                if (numberofstock<=stock_request_sender.BA):
                                    request_trade=tradereq.objects.create(
                                        sender=sender,
                                        receiver=receiver,action=action,
                                        stock=stock,
                                        numberofstocks=numberofstock,
                                        priceperstock=priceperstock,
                                        is_active=True,
                                    )
                                    return redirect('international:sentreq')
                                else:
                                    messages.error(request, f'Insufficient Stock holdings!!')
                            elif stock=='SBUX':
                                if (numberofstock<=stock_request_sender.SBUX):
                                    request_trade=tradereq.objects.create(
                                        sender=sender,
                                        receiver=receiver,action=action,
                                        stock=stock,
                                        numberofstocks=numberofstock,
                                        priceperstock=priceperstock,
                                        is_active=True,
                                    )
                                    return redirect('international:sentreq')
                                else:
                                    messages.error(request, f'Insufficient Stock holdings!!')
                            elif stock=='APL':
                                if (numberofstock<=stock_request_sender.APL):
                                    request_trade=tradereq.objects.create(
                                        sender=sender,
                                        receiver=receiver,action=action,
                                        stock=stock,
                                        numberofstocks=numberofstock,
                                        priceperstock=priceperstock,
                                        is_active=True,
                                    )
                                    return redirect('international:sentreq')
                                else:
                                    messages.error(request, f'Insufficient Stock holdings!!')
                            elif stock=='TSLA':
                                if (numberofstock<=stock_request_sender.TSLA):
                                    request_trade=tradereq.objects.create(
                                        sender=sender,
                                        receiver=receiver,action=action,
                                        stock=stock,
                                        numberofstocks=numberofstock,
                                        priceperstock=priceperstock,
                                        is_active=True,
                                    )
                                    return redirect('international:sentreq')
                                else:
                                    messages.error(request, f'Insufficient Stock holdings!!')
                            elif stock=='GOOGL':
                                if (numberofstock<=stock_request_sender.GOOGL):
                                    request_trade=tradereq.objects.create(
                                        sender=sender,
                                        receiver=receiver,action=action,
                                        stock=stock,
                                        numberofstocks=numberofstock,
                                        priceperstock=priceperstock,
                                        is_active=True,
                                    )
                                    return redirect('international:sentreq')
                                else:
                                    messages.error(request, f'Insufficient Stock holdings!!')
                            elif stock=='TMUS':
                                if (numberofstock<=stock_request_sender.TMUS):
                                    request_trade=tradereq.objects.create(
                                        sender=sender,
                                        receiver=receiver,action=action,
                                        stock=stock,
                                        numberofstocks=numberofstock,
                                        priceperstock=priceperstock,
                                        is_active=True,
                                    )
                                    return redirect('international:sentreq')
                                else:
                                    messages.error(request, f'Insufficient Stock holdings!!')  
                            elif stock=='GS':
                                if (numberofstock<=stock_request_sender.GS):
                                    request_trade=tradereq.objects.create(
                                        sender=sender,
                                        receiver=receiver,action=action,
                                        stock=stock,
                                        numberofstocks=numberofstock,
                                        priceperstock=priceperstock,
                                        is_active=True,
                                    )
                                    return redirect('international:sentreq')
                                else:
                                    messages.error(request, f'Insufficient Stock holdings!!')
                            elif stock=='GM':
                                if (numberofstock<=stock_request_sender.GM):
                                    request_trade=tradereq.objects.create(
                                        sender=sender,
                                        receiver=receiver,action=action,
                                        stock=stock,
                                        numberofstocks=numberofstock,
                                        priceperstock=priceperstock,
                                        is_active=True,
                                    )
                                    return redirect('international:sentreq')
                                else:
                                    messages.error(request, f'Insufficient Stock holdings!!')
                            elif stock=='KO':
                                if (numberofstock<=stock_request_sender.KO):
                                    request_trade=tradereq.objects.create(
                                        sender=sender,
                                        receiver=receiver,action=action,
                                        stock=stock,
                                        numberofstocks=numberofstock,
                                        priceperstock=priceperstock,
                                        is_active=True,
                                    )
                                    return redirect('international:sentreq')
                                else:
                                    messages.error(request, f'Insufficient Stock holdings!!')
                            elif stock=='TGT':
                                if (numberofstock<=stock_request_sender.TGT):
                                    request_trade=tradereq.objects.create(
                                        sender=sender,
                                        receiver=receiver,action=action,
                                        stock=stock,
                                        numberofstocks=numberofstock,
                                        priceperstock=priceperstock,
                                        is_active=True,
                                    )
                                    return redirect('international:sentreq')
                                else:
                                    messages.error(request, f'Insufficient Stock holdings!!')

                    else:
                        messages.error(request, f'You cannot Buy/Sell at price greater/lower than 10% of market price!')
                else:
                    messages.error(request, f'Please select another Rceiver!')        
    return render(request,'international/create_request.html',{'form':tradereqform})
@login_required
def report(request):
    form = reportform()
    if request.method=='POST':
        form = reportform(request.POST or None)
        if form.is_valid():
            obj = Report()
            obj.reporter=request.user
            obj.reporting=form.cleaned_data.get('reporting')
            print(obj.reporter)
            print(obj.reporting)
            obj.save()
        else:
            form=reportform()
        return redirect('international:dashboard')
    return render(request, 'international/report.html', {'form':form})
@login_required
def received_request(request):
    user=request.user
    requests_pending=tradereq.objects.order_by('-id').filter(receiver=user,is_active=True)
    return render(request,'international/received_request.html',{'requests':requests_pending})

@login_required
def sent_request(request):
    user=request.user
    sent_pending=tradereq.objects.order_by('-id').filter(sender=user,is_active=True)
    return render(request,'international/sent_requests.html',{'requests':sent_pending})

@login_required
def history(request):
    user=request.user
    transactions=tradereq.objects.order_by('-id').filter(sender=user)
    return render(request,'international/transaction-history.html',{'requests':transactions})


@login_required
def all_history(request):
    user=request.user
    #transactions=tradereq.objects.order_by('-id').filter(Q(receiver=user) | Q(sender=user))
    comb_query = tradereq.objects.filter(sender=user) | tradereq.objects.filter(receiver=user)
    final_query = comb_query.filter(status='accepted')
    transactions=final_query.order_by('-id')
    return render(request,'international/transaction-log.html',{'requests':transactions})


"""
@login_required
def accept_request(request,*args, **kwargs):
    user=request.user
    payload={}
    if request.method=='GET':
        tradereq_id=kwargs.get("friend_request_id")
        if tradereq_id:
            trade_request=tradereq.objects.id(pk=tradereq_id)
            if trade_request.receiver==user:
                if trade_request:
                    trade_request.accept()
                    payload['response']="request accepted"
                else:
                    payload['response']="something went wrong"
            else:
                payload['response']="not yours request"
        else:
            payload['response']="unable not accepted"
    else:
        payload['response']="you must be authenticated to accpet a friend request"
    return HttpResponse(json.dumps(payload),content_type="application/json")
"""

@login_required 
def accept_request(request,*args, **kwargs):
    user =request.user
    if request.method=='GET':
        tradereq_id=kwargs.get("friend_request_id")
        if tradereq_id:
            trade_request=tradereq.objects.filter(pk=tradereq_id)[0]
            if trade_request:
                mess = trade_request.accept()
                print(mess)
                messages.error(request, mess)
                return redirect("international:receivedreq")

@login_required
def decline_request(request,*args, **kwargs):
    user=request.user
    if request.method=='GET':
        tradereq_id=kwargs.get("friend_request_id")
        if tradereq_id:
            trade_request=tradereq.objects.filter(pk=tradereq_id)[0]
            if trade_request:
                trade_request.decline()
                return redirect("international:receivedreq")


@login_required
def cancel_request(request,*args, **kwargs):
    user=request.user
    if request.method=='GET':
        tradereq_id=kwargs.get("friend_request_id")
        if tradereq_id:
            trade_request=tradereq.objects.filter(pk=tradereq_id)[0]
            if trade_request:
                trade_request.cancel()
                return redirect("international:sentreq")


