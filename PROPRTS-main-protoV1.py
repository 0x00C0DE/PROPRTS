import robin_stocks
import math
import pyotp
import sched
import time
import datetime
import sys
import numpy as np
import matplotlib.pyplot as plt
import sched
from scipy import stats
from datetime import datetime, timedelta

# Program description:
# A Robinhood bot created to automatically monitor and trade crypto currency currently supported by Robinhood.
# Works specifically for DOGE, but can work for other tokens that have miniscule values.
#
# This bot runs a scheduler every 10 seconds in order to update the prices on a 10 second interval for a 
# list that will hold the previous prices for past 1 minute.
# 
# This bot [REQUIRES] a individual to already have SET amount of shares of the current crypto they want to trade.
# 
#   Instructions after entering in login information (no particular order):
#
#       1. Fill in ticker (since this bot is specifically for DOGE, should be left alone)
#       2. Fill in average_cost
#       3. Fill in Shares2Buy amount (in dollars $)
#       4. Fill in Shares2Sell amount (in dollars $)
#       5. Fill in num_shares 
#

# Some buying and selling errors will occur if a individual does not have enough shares to sell or enough money to buy.
# If errors occur, simply re-update through redoing instructions above and restart the program.


# Robinhood.login(username="example72", password="AnotherExample8")
totp = pyotp.TOTP("Sauce").now()
login = robin_stocks.login("email_here@test.com", "password_here")

# Scheduler created to run every n seconds
s = sched.scheduler(time.time, time.sleep)

# 10 second interval price history list, for every 1 minute
historicalPrices = []
reorderArray = []

# keeps track of the number of runs since the start of the program
numOfRuns = 1.0

Shares2Sell = 0.00

# static amount of shares you want to sell in dollar amount
shares2sellDollar = 12

# ratio of buy to sell 2:6 ≈ 1:3
updateSharesSell = 3


Shares2Buy = 0.00
# static amount of shares you want to buy in dollar amount
shares2buyDollar = 4

# ratio of buy to sell 2:6 ≈ 1:3
updateSharesBuy = 1

# step (5)
# number of shares based on (total cost / Shares2Buy)
# EX: ($100 / 2) = 50
num_shares = 9
# step (2)
# average cost
average_cost = 1.24

# average cost ceiling percentage (ensures there is a large enough disparity between the live price and the required minimal amount that is greater than the live price to obtain profitability when selling)
# average cost floor percentage(ensures there is a large enough disparity between the live price and the required minimal amount that is lower than the live price to obtain profitability when buying)
ac_ceiling = 0.01
ac_floor = 0.0075
y = []
yy = []
x = []
xx = []
pastPredictionMinutesAhead1 = []
pastPredictionPrice1 = []
pastPredictionDate1 = []

xyz1flag1 = False
xyz1flag2 = False
xyz1flag5 = False
xyz1flag15 = False
xyz1flag30 = False
xyz1flag60 = False
xyz1flag120 = False

count = 0
tempcounter = 1
tempcounter2 = 1
priceCompareBuyFlag = False
priceCompareSellFlag = False
cryptoSymbol = 0
def run(sc):

    global priceCompareBuyFlag
    global priceCompareSellFlag
    global historicalPrices 
    global reorderArray
    global x
    global xx
    global y
    global yy
    global ac_ceiling
    global ac_floor
    global updateSharesSell
    global updateSharesBuy
    global pastPredictionMinutesAhead1
    global pastPredictionPrice1
    global pastPredictionDate1
    global cryptoSymbol
    global Shares2Sell
    global Shares2Buy
    global numOfRuns
    global average_cost
    global num_shares

    global xyz1flag1
    global xyz1flag2
    global xyz1flag5
    global xyz1flag15
    global xyz1flag30
    global xyz1flag60
    global xyz1flag120

    global count

    lrData1 = 'PROPRTS-1-LR-data.txt'
    
    # Using readlines()
    file1 = open(lrData1, 'r')
    Lines = file1.readlines()

    # Strips the newline character
    for line in Lines:
        line = line.replace('(','').replace(')','')
        line = line.replace(',', '')
        line = line.split()
        xx.append(line[0])
        xx = [float(i) for i in xx]
        yy.append(line[1])
        yy = [float(i) for i in yy]
    file1.close()
    x.clear()
    y.clear()
    x = xx
    y = yy
        
    # crypto currency ticker available on robinhood
    ticker = "MATIC"
    
    cryptoSymbol = robin_stocks.crypto.get_crypto_quote(ticker, info="mark_price")
    #cryptoSymbol = robin_stocks.robinhood.get_latest_price(ticker)
    print(ticker + ": $" + str(cryptoSymbol))

    historicalPrices.append(cryptoSymbol)

    if len(historicalPrices) > 6:

        # if there are 7 or more elements in the list, rearrange positions
        reorderArray = historicalPrices[1:7]
        historicalPrices = historicalPrices[-1:]

        historicalPrices = reorderArray + historicalPrices
        print("Cleared and repositioned")

    if len(historicalPrices) == 1:
        #0sec
        print("appended historicalPrices[0]")
        print(historicalPrices)
    elif len(historicalPrices) == 2:
        print("appended historicalPrices[1]")
        print(historicalPrices)
    elif len(historicalPrices) == 3:
        print("appended historicalPrices[2]")
        print(historicalPrices)
    elif len(historicalPrices) == 4:
        print("appended historicalPrices[3]")
        print(historicalPrices)
    elif len(historicalPrices) == 5:
        print("appended historicalPrices[4]")
        print(historicalPrices)
    elif len(historicalPrices) == 6:
        print("appended historicalPrices[5]")
        print(historicalPrices)
    elif len(historicalPrices) == 7:
        print("appended historicalPrices[6]")
        print(historicalPrices)

    
    linear_Regression(x, y, pastPredictionMinutesAhead1, pastPredictionPrice1, pastPredictionDate1)
    #print("pastPredictionMinutesAhead1 : ", pastPredictionMinutesAhead1)
    pastPredictionMinutesAhead1, pastPredictionPrice1, pastPredictionDate1 = removeExpiredPredictions(pastPredictionMinutesAhead1, pastPredictionPrice1, pastPredictionDate1)
    xyz1flag1, xyz1flag2,  xyz1flag5,  xyz1flag15,  xyz1flag30,  xyz1flag60,  xyz1flag120 = checkPastPredictions(pastPredictionMinutesAhead1, pastPredictionPrice1, pastPredictionDate1, cryptoSymbol, xyz1flag1, xyz1flag2,  xyz1flag5,  xyz1flag15,  xyz1flag30,  xyz1flag60,  xyz1flag120)
    '''
    Beginning of price comparison pecentage change algorithm section
    '''
    # BUY
    if numOfRuns < 7:
        
        if numOfRuns == 6: 
            if float(historicalPrices[0])*0.993 > float(cryptoSymbol) and float(cryptoSymbol) < float(average_cost-float(average_cost*float(ac_floor))):

                # instruction step (3) fill in amount in dollars in place of float(20)
                priceCompareBuyFlag = True
                
        elif numOfRuns == 5:
            if float(historicalPrices[0])*0.994 > float(cryptoSymbol) and float(cryptoSymbol) < float(average_cost-float(average_cost*float(ac_floor))):
                
                # instruction step (3) fill in amount in dollars in place of float(20)
                priceCompareBuyFlag = True

        elif numOfRuns == 4:
            if float(historicalPrices[0])*0.995 > float(cryptoSymbol) and float(cryptoSymbol) < float(average_cost-float(average_cost*float(ac_floor))):

                # instruction step (3) fill in amount in dollars in place of float(20)
                priceCompareBuyFlag = True
                
        elif numOfRuns == 3:
            if float(historicalPrices[0])*0.996 > float(cryptoSymbol) and float(cryptoSymbol) < float(average_cost-float(average_cost*float(ac_floor))):

                # instruction step (3) fill in amount in dollars in place of float(20)
                priceCompareBuyFlag = True
                
        elif numOfRuns == 2:
            if float(historicalPrices[0])*0.997 > float(cryptoSymbol) and float(cryptoSymbol) < float(average_cost-float(average_cost*float(ac_floor))):

                # instruction step (3) fill in amount in dollars in place of float(20)
                priceCompareBuyFlag = True

    #BUY
    if numOfRuns >= 7:

        if float(cryptoSymbol)*1.07 < float(historicalPrices[0]) and float(cryptoSymbol) < float(average_cost-float(average_cost*float(ac_floor))):

            # instruction step (3) fill in amount in dollars in place of float(20)
            priceCompareBuyFlag = True

        elif float(cryptoSymbol)*1.006 < float(historicalPrices[1]) and float(cryptoSymbol) < float(average_cost-float(average_cost*float(ac_floor))):

            # instruction step (3) fill in amount in dollars in place of float(20)
            priceCompareBuyFlag = True
            
        elif float(cryptoSymbol)*1.005 < float(historicalPrices[2]) and float(cryptoSymbol) < float(average_cost-float(average_cost*float(ac_floor))):

            # instruction step (3) fill in amount in dollars in place of float(20)
            priceCompareBuyFlag = True
            
        elif float(cryptoSymbol)*1.004 < float(historicalPrices[3]) and float(cryptoSymbol) < float(average_cost-float(average_cost*float(ac_floor))):

            # instruction step (3) fill in amount in dollars in place of float(20)
            priceCompareBuyFlag = True
            
        elif float(cryptoSymbol)*1.003 < float(historicalPrices[4]) and float(cryptoSymbol) < float(average_cost-float(average_cost*float(ac_floor))):

            # instruction step (3) fill in amount in dollars in place of float(20)
            priceCompareBuyFlag = True
            
        elif float(cryptoSymbol)*1.002 < float(historicalPrices[5]) and float(cryptoSymbol) < float(average_cost-float(average_cost*float(ac_floor))):

            # instruction step (3) fill in amount in dollars in place of float(20)
            priceCompareBuyFlag = True
            
    #SELL
    if numOfRuns < 7:
                
        if numOfRuns == 6:
            if float(historicalPrices[0])*1.007 < float(cryptoSymbol) and float(cryptoSymbol) > float(average_cost+float(average_cost*float(ac_ceiling))):

                # instruction step (4) fill in amount in dollars in place of float(100)
                priceCompareSellFlag = True
                
        elif numOfRuns == 5:
            if float(historicalPrices[0])*1.006 < float(cryptoSymbol) and float(cryptoSymbol) > float(average_cost+float(average_cost*float(ac_ceiling))):

                # instruction step (4) fill in amount in dollars in place of float(100)
                priceCompareSellFlag = True
                
        elif numOfRuns == 4:
            if float(historicalPrices[0])*1.005 < float(cryptoSymbol) and float(cryptoSymbol) > float(average_cost+float(average_cost*float(ac_ceiling))):

                # instruction step (4) fill in amount in dollars in place of float(100)
                priceCompareSellFlag = True
                
        elif numOfRuns == 3:
            if float(historicalPrices[0])*1.004 < float(cryptoSymbol) and float(cryptoSymbol) > float(average_cost+float(average_cost*float(ac_ceiling))):

                # instruction step (4) fill in amount in dollars in place of float(100)
                priceCompareSellFlag = True
                
        elif numOfRuns == 2:
            if float(historicalPrices[0])*1.003 < float(cryptoSymbol) and float(cryptoSymbol) > float(average_cost+float(average_cost*float(ac_ceiling))):

                # instruction step (4) fill in amount in dollars in place of float(100)
                priceCompareSellFlag = True

    #SELL
    if numOfRuns >= 7:

        if float(cryptoSymbol)*0.993 > float(historicalPrices[0]) and float(cryptoSymbol) > float(average_cost+float(average_cost*float(ac_ceiling))):

            # instruction step (4) fill in amount in dollars in place of float(100)
            priceCompareSellFlag = True
        
        elif float(cryptoSymbol)*0.994 > float(historicalPrices[1]) and float(cryptoSymbol) > float(average_cost+float(average_cost*float(ac_ceiling))):

            # instruction step (4) fill in amount in dollars in place of float(100)
            priceCompareSellFlag = True
            
        elif float(cryptoSymbol)*0.995 > float(historicalPrices[2]) and float(cryptoSymbol) > float(average_cost+float(average_cost*float(ac_ceiling))):

            # instruction step (4) fill in amount in dollars in place of float(100)
            priceCompareSellFlag = True
            
        elif float(cryptoSymbol)*0.996 > float(historicalPrices[3]) and float(cryptoSymbol) > float(average_cost+float(average_cost*float(ac_ceiling))):

            # instruction step (4) fill in amount in dollars in place of float(100)
            priceCompareSellFlag = True
            
        elif float(cryptoSymbol)*0.997 > float(historicalPrices[4]) and float(cryptoSymbol) > float(average_cost+float(average_cost*float(ac_ceiling))):

            # instruction step (4) fill in amount in dollars in place of float(100)
            priceCompareSellFlag = True
            
        elif float(cryptoSymbol)*0.998 > float(historicalPrices[5]) and float(cryptoSymbol) > float(average_cost+float(average_cost*float(ac_ceiling))):

            # instruction step (4) fill in amount in dollars in place of float(100)
            priceCompareSellFlag = True

    '''
    End of price comparison pecentage change algorithm section
    '''
    print("status of priceCompareSellFlag: ", priceCompareSellFlag)
    print("status of xyz1flag1: ", xyz1flag1)
    print("status of xyz1flag2: ", xyz1flag2)
    print("status of xyz1flag5: ", xyz1flag5)
    print("status of xyz1flag15: ", xyz1flag15)
    print("status of xyz1flag30: ", xyz1flag30)
    print("status of xyz1flag60: ", xyz1flag60)
    print("status of xyz1flag120: ", xyz1flag120)
    
    if priceCompareSellFlag == True and xyz1flag1 == True and xyz1flag2 == True and xyz1flag5 == True:
        Shares2Sell = math.floor((float(shares2sellDollar)) / (float(cryptoSymbol)))
        crypto_SELL(ticker, Shares2Sell)
        print("sold:", cryptoSymbol)
        print("avg cost:", average_cost)
        num_shares -= updateSharesSell

    if priceCompareSellFlag == True and xyz1flag15 == True and xyz1flag30 == True and xyz1flag60 == True and xyz1flag120 == True:
        Shares2Sell = math.floor((float(shares2sellDollar)) / (float(cryptoSymbol)))
        crypto_SELL(ticker, Shares2Sell)
        print("sold:", cryptoSymbol)
        print("avg cost:", average_cost)
        num_shares -= updateSharesSell
    if priceCompareBuyFlag == True:
        Shares2Buy = math.floor((float(shares2buyDollar)) / (float(cryptoSymbol)))
        crypto_BUY(ticker, Shares2Buy)
        print("bought:", cryptoSymbol)
        tempval = average_cost*num_shares
        average_cost = tempval
        average_cost += float(cryptoSymbol)*float(1.0039)
        num_shares += updateSharesBuy
        average_cost /= float(num_shares)
        print("avg cost:" + str(average_cost))
    
    xyz1flag1 = False
    xyz1flag2 = False
    xyz1flag5 = False
    xyz1flag15 = False
    xyz1flag30 = False
    xyz1flag60 = False
    xyz1flag120 = False
    priceCompareSellFlag = False
    priceCompareBuyFlag = False

    # Keeps track of counter
    print("numOfRuns:" + str(numOfRuns))
    numOfRuns += 1
    
    # calls scheduler every 10 seconds
    s.enter(60, 1, run, (sc,))

# Functions to buy and sell crypto currency   
def crypto_BUY(ticker, amountD):
    cryptoSymbol = robin_stocks.orders.order_buy_crypto_by_quantity(ticker, float(amountD), timeInForce='gtc')
    print(cryptoSymbol)

def crypto_SELL(ticker, amountD):
    cryptoSymbol = robin_stocks.orders.order_sell_crypto_by_quantity(ticker, float(amountD), timeInForce='gtc')
    print(cryptoSymbol)

def myfunc(x):
    return slope * x + intercept

def removeExpiredPredictions(pm, pp, pd):

    if len(pd) > 0:
        count = -1
        for i in pd:
            checkResflag1 = False
            checkResflag2 = False
            dt = datetime.now()
            result = i - dt
            stringRes = str(result)
            checkRes = stringRes[0]
            count += 1
            if checkRes == '-':
                pd.remove(i)
                checkResflag1 = True
                checkResflag2 = True
            if checkResflag1 == True:
                del pp[count]
                checkResflag1 = False
            if checkResflag2 == True:
                del pm[count]
                checkResflag2 = False
    return (pm, pp, pd)

def checkPastPredictions(pm, pp, pd, cryptoPrice, f1, f2, f5, f15, f30, f60, f120):
    pp = [float(i) for i in pp]
    for i in range(len(pp)):
        if float(cryptoPrice) >= pp[i]:
            if pm[i] == 1:
                f1 = True
            if pm[i] == 2:
                f2 = True
            if pm[i] == 5:
                f5 = True
            if pm[i] == 15:
                f15 = True
            if pm[i] == 30:
                f30 = True
            if pm[i] == 60:
                f60 = True
            if pm[i] == 120:
                f120 = True
    return (f1, f2, f5, f15, f30, f60, f120)

def linear_Regression(xx, yy, pm, pp, pd):
    '''
    Beginning of linear regression section
    '''
    global tempcounter
    global tempcounter2
    
    global slope
    global intercept
    global r
    global p
    global std_err
    x = []
    y = []

    for i in xx:
        x.append(i)
    x = [float(i) for i in x]
    for i in yy:
        y.append(i)
    y = [float(i) for i in y]
    slope, intercept, r, p, std_err = stats.linregress(x, y)
    mymodel = list(map(myfunc, x))
    price_prediction(pm, pp, pd)
    
    print("slope:", slope)
    print("intercept:", intercept)
    print("r:", r)
    print("p:", p)
    print("std_err:", std_err)
    
    plt.clf()
    plt.scatter(x, y)
    plt.plot(x, mymodel)
    plt.title("PROPRTS-main-1-V1")
    plt.savefig("main_lr_protoV1.png")

    '''
    End of linear regression section
    '''

def price_prediction(m, p, d):
    
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    predictionMinutesAhead = dt + timedelta(minutes = 120)
    pts = datetime.timestamp(predictionMinutesAhead)
    price = myfunc(pts)
    m.append(((pts-ts)/60))
    p.append(price)
    d.append(predictionMinutesAhead)
    print("\nprice prediction", ((pts-ts)/60), "minutes ahead from now:$", price, " [ " , predictionMinutesAhead , " ] ")
    predictionMinutesAhead2 = dt + timedelta(minutes = 60)
    pts2 = datetime.timestamp(predictionMinutesAhead2)
    price2 = myfunc(pts2)
    m.append(((pts2-ts)/60))
    p.append(price2)
    d.append(predictionMinutesAhead2)
    print("price prediction", ((pts2-ts)/60), "minutes ahead from now:$", price2, " [ " , predictionMinutesAhead2 , " ] ")
    predictionMinutesAhead3 = dt + timedelta(minutes = 30)
    pts3 = datetime.timestamp(predictionMinutesAhead3)
    price3 = myfunc(pts3)
    m.append(((pts3-ts)/60))
    p.append(price3)
    d.append(predictionMinutesAhead3)
    print("price prediction", ((pts3-ts)/60), "minutes ahead from now:$", price3, " [ " , predictionMinutesAhead3 , " ] ")
    predictionMinutesAhead4 = dt + timedelta(minutes = 15)
    pts4 = datetime.timestamp(predictionMinutesAhead4)
    price4 = myfunc(pts4)
    m.append(((pts4-ts)/60))
    p.append(price4)
    d.append(predictionMinutesAhead4)
    print("price prediction", ((pts4-ts)/60), "minutes ahead from now:$", price4, " [ " , predictionMinutesAhead4 , " ] ")
    predictionMinutesAhead5 = dt + timedelta(minutes = 5)
    pts5 = datetime.timestamp(predictionMinutesAhead5)
    price5 = myfunc(pts5)
    m.append(((pts5-ts)/60))
    p.append(price5)
    d.append(predictionMinutesAhead5)
    print("price prediction", ((pts5-ts)/60), "minutes ahead from now:$", price5, " [ " , predictionMinutesAhead5 , " ] ")
    predictionMinutesAhead6 = dt + timedelta(minutes = 2)
    pts6 = datetime.timestamp(predictionMinutesAhead6)
    price6 = myfunc(pts6)
    m.append(((pts6-ts)/60))
    p.append(price6)
    d.append(predictionMinutesAhead6)
    print("price prediction", ((pts6-ts)/60), "minutes ahead from now:$", price6, " [ " , predictionMinutesAhead6 , " ] ")
    predictionMinutesAhead7 = dt + timedelta(minutes = 1)
    pts7 = datetime.timestamp(predictionMinutesAhead7)
    price7 = myfunc(pts7)
    m.append(((pts7-ts)/60))
    p.append(price7)
    d.append(predictionMinutesAhead7)
    print("price prediction", ((pts7-ts)/60), "minutes ahead from now:$", price7, " [ " , predictionMinutesAhead7 , " ] ", "\n")

    print("current time: ", dt, "\n")

s.enter(1, 1, run, (s,))
while True:
    try:
        s.run()
    except:
        pass
