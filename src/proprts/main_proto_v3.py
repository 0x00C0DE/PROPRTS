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
from time import sleep

# Program description:
# A Robinhood bot created to automatically monitor and trade crypto currency currently supported by Robinhood.
#
# This bot runs a scheduler every 60 seconds in order to update the prices on a 60 second interval for a 
# list that will hold the previous prices for past 6 minute.
# 
# This bot [REQUIRES] a individual to already have SET amount of shares of the current crypto they want to trade.
# 
#   Instructions after entering in login information (no particular order):
#
#       1. Fill in ticker
#       2. Fill in average_cost
#       3. Fill in Shares2Buy amount (in dollars $)
#       4. Fill in Shares2Sell amount (in dollars $)
#       5. Fill in num_shares 
#

# Some buying and selling errors will occur if a individual does not have enough shares to sell or enough money to buy.
# If errors occur, simply re-update through redoing instructions above and restart the program.

class CryptoBot:
    totp = pyotp.TOTP("Sauce").now()
    login = robin_stocks.login("email_here@test.com", "Password_here")
    historicalPrices = []
    reorderArray = []
    numOfRuns = 1.0
    Shares2Sell = 0.00
    shares2sellDollar = 9
    updateSharesSell = 0
    Shares2Buy = 0.00
    shares2buyDollar = 10
    updateSharesBuy = 0
    num_shares = 194.9839
    average_cost = 1.26
    ac_ceiling = 0.0075
    ac_floor = 0.02
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

    slope = 0
    intercept = 0
    r = 0
    p = 0
    std_err = 0
    count = 0
    tempcounter = 1
    tempcounter2 = 1
    priceCompareBuyFlag = False
    priceCompareSellFlag = False
    cryptoPrice = 0
    ticker = "MATIC"
    lrData1 = 'PROPRTS-1-LRv2-data.txt'


    def main_trigger(self):
        self.get_crypto_quote()
        self.read_lr_data()
        self.removeExpiredPredictions()
        self.checkPastPredictions()
        self.check_sell_flag()
        self.check_buy_flag()
        self.xyz1flag1 = False
        self.xyz1flag2 = False
        self.xyz1flag5 = False
        self.xyz1flag15 = False
        self.xyz1flag30= False
        self.xyz1flag60 = False
        self.xyz1flag120 = False
        self.priceCompareSellFlag = False
        self.priceCompareBuyFlag = False
        
    def read_lr_data(self):
        file1 = open(self.lrData1, 'r')
        Lines = file1.readlines()

        for line in Lines:
            line = line.replace('(','').replace(')','')
            line = line.replace(',', '')
            line = line.split()
            self.xx.append(line[0])
            self.xx = [float(i) for i in self.xx]
            self.yy.append(line[1])
            self.yy = [float(i) for i in self.yy]
        file1.close()
        self.x.clear()
        self.y.clear()
        self.x = [float(i) for i in self.xx]
        self.y = [float(i) for i in self.yy]
        print("self.x : ", self.x)
        print("self.y : ", self.y)
        self.xx.clear()
        self.yy.clear()
        self.linear_Regression(self.x, self.y)
        
    def get_crypto_quote(self):
        self.cryptoPrice = robin_stocks.crypto.get_crypto_quote(self.ticker, info="mark_price")
        print(self.ticker + ": $" + str(self.cryptoPrice))
        self.historicalPrices.append(self.cryptoPrice)

        if len(self.historicalPrices) > 6:
            self.reorderArray = self.historicalPrices[1:7]
            self.historicalPrices = self.historicalPrices[-1:]
            self.historicalPrices = self.reorderArray + self.historicalPrices
            print("Cleared and repositioned")

        if len(self.historicalPrices) == 1:
            print("appended historicalPrices[0]")
            print(self.historicalPrices)
        elif len(self.historicalPrices) == 2:
            print("appended historicalPrices[1]")
            print(self.historicalPrices)
        elif len(self.historicalPrices) == 3:
            print("appended historicalPrices[2]")
            print(self.historicalPrices)
        elif len(self.historicalPrices) == 4:
            print("appended historicalPrices[3]")
            print(self.historicalPrices)
        elif len(self.historicalPrices) == 5:
            print("appended historicalPrices[4]")
            print(self.historicalPrices)
        elif len(self.historicalPrices) == 6:
            print("appended historicalPrices[7]")
            print(self.historicalPrices)

        print("status of priceCompareBuyFlag: ", self.priceCompareBuyFlag)
        print("status of priceCompareSellFlag: ", self.priceCompareSellFlag)
        print("status of xyz1flag1: ", self.xyz1flag1)
        print("status of xyz1flag2: ", self.xyz1flag2)
        print("status of xyz1flag5: ", self.xyz1flag5)
        print("status of xyz1flag15: ", self.xyz1flag15)
        print("status of xyz1flag30: ", self.xyz1flag30)
        print("status of xyz1flag60: ", self.xyz1flag60)
        print("status of xyz1flag120: ", self.xyz1flag120)
        print("the numOfRuns is: ", str(self.numOfRuns))

        # Keeps track of counter
        self.numOfRuns += 1



    def linear_Regression(self, x, y):
        '''
        Beginning of linear regression section
        '''
        print("LR x: ", x)
        print("LR y: ", y)
        #x = [float(i) for i in self.xx]
        #print("x: ", self.xx)
        #y = [float(i) for i in self.yy]
        #print("y: ", self.yy)
        self.slope, self.intercept, self.r, self.p, self.std_err = stats.linregress(x, y)

        mymodel = list(map(self.myfunc, x))

        self.price_prediction(self.pastPredictionMinutesAhead1, self.pastPredictionPrice1, self.pastPredictionDate1)

        print("slope:", self.slope)
        print("intercept:", self.intercept)
        print("r:", self.r)
        print("p:", self.p)
        print("std_err:", self.std_err)

        plt.clf()
        plt.scatter(x, y)
        plt.plot(x, mymodel)
        plt.savefig("tempmain_linear_regression.png")
        '''
        End of linear regression section
        '''


    def myfunc(self, x):
        return self.slope * x + self.intercept

    def removeExpiredPredictions(self):
        if len(self.pastPredictionDate1) > 0:
            count = -1
            for i in self.pastPredictionDate1:
                checkResflag1 = False
                checkResflag2 = False
                dt = datetime.now()
                result = i - dt
                stringRes = str(result)
                checkRes = stringRes[0]
                count += 1
                if checkRes == '-':
                    self.pastPredictionDate1.remove(i)
                    checkResflag1 = True
                    checkResflag2 = True
                if checkResflag1 == True:
                    del self.pastPredictionPrice1[count]
                    checkResflag1 = False
                if checkResflag2 == True:
                    del self.pastPredictionMinutesAhead1[count]
                    checkResflag2 = False
        return (self.pastPredictionMinutesAhead1, self.pastPredictionPrice1, self.pastPredictionDate1)

    def checkPastPredictions(self):
        self.pastPredictionPrice1 = [float(i) for i in self.pastPredictionPrice1]
        for i in range(len(self.pastPredictionPrice1)):
            if float(self.cryptoPrice) >= self.pastPredictionPrice1[i]:

                if self.pastPredictionMinutesAhead1[i] == 1:
                    self.f1 = True

                if self.pastPredictionMinutesAhead1[i] == 2:
                    self.f2 = True
      
                if self.pastPredictionMinutesAhead1[i] == 5:
                    self.f5 = True
      
                if self.pastPredictionMinutesAhead1[i] == 15:
                    self.f15 = True
       
                if self.pastPredictionMinutesAhead1[i] == 30:
                    self.f30 = True

                if self.pastPredictionMinutesAhead1[i] == 60:
                    self.f60 = True
        
                if self.pastPredictionMinutesAhead1[i] == 120:
                    self.f120 = True

        return (self.f1, self.f2, self.f5, self.f15, self.f30, self.f60, self.f120)



    def price_prediction(self, m, p, d):
        
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        predictionMinutesAhead = dt + timedelta(minutes = 120)
        pts = datetime.timestamp(predictionMinutesAhead)
        price = self.myfunc(pts)
        m.append(((pts-ts)/60))
        p.append(price)
        d.append(predictionMinutesAhead)
        print("\nprice prediction", ((pts-ts)/60), "minutes ahead from now:$", price, " [ " , predictionMinutesAhead , " ] ")
        predictionMinutesAhead2 = dt + timedelta(minutes = 60)
        pts2 = datetime.timestamp(predictionMinutesAhead2)
        price2 = self.myfunc(pts2)
        m.append(((pts2-ts)/60))
        p.append(price2)
        d.append(predictionMinutesAhead2)
        print("price prediction", ((pts2-ts)/60), "minutes ahead from now:$", price2, " [ " , predictionMinutesAhead2 , " ] ")
        predictionMinutesAhead3 = dt + timedelta(minutes = 30)
        pts3 = datetime.timestamp(predictionMinutesAhead3)
        price3 = self.myfunc(pts3)
        m.append(((pts3-ts)/60))
        p.append(price3)
        d.append(predictionMinutesAhead3)
        print("price prediction", ((pts3-ts)/60), "minutes ahead from now:$", price3, " [ " , predictionMinutesAhead3 , " ] ")
        predictionMinutesAhead4 = dt + timedelta(minutes = 15)
        pts4 = datetime.timestamp(predictionMinutesAhead4)
        price4 = self.myfunc(pts4)
        m.append(((pts4-ts)/60))
        p.append(price4)
        d.append(predictionMinutesAhead4)
        print("price prediction", ((pts4-ts)/60), "minutes ahead from now:$", price4, " [ " , predictionMinutesAhead4 , " ] ")
        predictionMinutesAhead5 = dt + timedelta(minutes = 5)
        pts5 = datetime.timestamp(predictionMinutesAhead5)
        price5 = self.myfunc(pts5)
        m.append(((pts5-ts)/60))
        p.append(price5)
        d.append(predictionMinutesAhead5)
        print("price prediction", ((pts5-ts)/60), "minutes ahead from now:$", price5, " [ " , predictionMinutesAhead5 , " ] ")
        predictionMinutesAhead6 = dt + timedelta(minutes = 2)
        pts6 = datetime.timestamp(predictionMinutesAhead6)
        price6 = self.myfunc(pts6)
        m.append(((pts6-ts)/60))
        p.append(price6)
        d.append(predictionMinutesAhead6)
        print("price prediction", ((pts6-ts)/60), "minutes ahead from now:$", price6, " [ " , predictionMinutesAhead6 , " ] ")
        predictionMinutesAhead7 = dt + timedelta(minutes = 1)
        pts7 = datetime.timestamp(predictionMinutesAhead7)
        price7 = self.myfunc(pts7)
        m.append(((pts7-ts)/60))
        p.append(price7)
        d.append(predictionMinutesAhead7)
        print("price prediction", ((pts7-ts)/60), "minutes ahead from now:$", price7, " [ " , predictionMinutesAhead7 , " ] ", "\n")

        print("current time: ", dt, "\n")

    # Functions to buy and sell crypto currency   
    def crypto_BUY(self, ticker, amountD):
        cryptoPrice = robin_stocks.orders.order_buy_crypto_by_quantity(ticker, float(amountD), timeInForce='gtc')
        print(cryptoPrice)
        print("ticker.state: ", cryptoPrice.state)
        return cryptoPrice

    def crypto_SELL(self, ticker, amountD):
        cryptoPrice = robin_stocks.orders.order_sell_crypto_by_quantity(ticker, float(amountD), timeInForce='gtc')
        print(cryptoPrice)
        print("ticker.state: ", cryptoPrice.state)
        return cryptoPrice
    
    '''
    Beginning of price comparison pecentage change algorithm section
    '''
    # BUY

    def buy(self):
        if self.numOfRuns < 7:
            
            if self.numOfRuns == 6: 
                if float(self.historicalPrices[0])*0.993 > float(self.cryptoPrice) and float(self.cryptoPrice) < float(self.average_cost-float(self.average_cost*float(self.ac_floor))):
                    priceCompareBuyFlag = True

            elif self.numOfRuns == 5:
                if float(self.historicalPrices[0])*0.994 > float(self.cryptoPrice) and float(self.cryptoPrice) < float(self.average_cost-float(self.average_cost*float(self.ac_floor))):
                    priceCompareBuyFlag = True

            elif self.numOfRuns == 4:
                if float(self.historicalPrices[0])*0.995 > float(self.cryptoPrice) and float(self.cryptoPrice) < float(self.average_cost-float(self.average_cost*float(self.ac_floor))):
                    priceCompareBuyFlag = True

            elif self.numOfRuns == 3:
                if float(self.historicalPrices[0])*0.996 > float(self.cryptoPrice) and float(self.cryptoPrice) < float(self.average_cost-float(self.average_cost*float(self.ac_floor))):
                    priceCompareBuyFlag = True

            elif self.numOfRuns == 2:
                if float(self.historicalPrices[0])*0.997 > float(self.cryptoPrice) and float(self.cryptoPrice) < float(self.average_cost-float(self.average_cost*float(self.ac_floor))):
                    priceCompareBuyFlag = True

        #BUY
        if self.numOfRuns >= 7:

            if float(self.cryptoPrice)*1.07 < float(self.historicalPrices[0]) and float(self.cryptoPrice) < float(self.average_cost-float(self.average_cost*float(self.ac_floor))):
                priceCompareBuyFlag = True

            elif float(self.cryptoPrice)*1.006 < float(self.historicalPrices[1]) and float(self.cryptoPrice) < float(self.average_cost-float(self.average_cost*float(self.ac_floor))):
                priceCompareBuyFlag = True

            elif float(self.cryptoPrice)*1.005 < float(self.historicalPrices[2]) and float(self.cryptoPrice) < float(self.average_cost-float(self.average_cost*float(self.ac_floor))):
                priceCompareBuyFlag = True

            elif float(self.cryptoPrice)*1.004 < float(self.historicalPrices[3]) and float(self.cryptoPrice) < float(self.average_cost-float(self.average_cost*float(self.ac_floor))):
                priceCompareBuyFlag = True
                
            elif float(self.cryptoPrice)*1.003 < float(self.historicalPrices[4]) and float(self.cryptoPrice) < float(self.average_cost-float(self.average_cost*float(self.ac_floor))):
                priceCompareBuyFlag = True

            elif float(self.cryptoPrice)*1.002 < float(self.historicalPrices[5]) and float(self.cryptoPrice) < float(self.average_cost-float(self.average_cost*float(self.ac_floor))):
                priceCompareBuyFlag = True
                
    #SELL
    def sell(self):
        if self.numOfRuns < 7:
                    
            if self.numOfRuns == 6:
                if float(self.historicalPrices[0])*1.007 < float(self.cryptoPrice) and float(self.cryptoPrice) > float(self.average_cost+float(self.average_cost*float(self.ac_ceiling))):
                    priceCompareSellFlag = True
                    
            elif self.numOfRuns == 5:
                if float(self.historicalPrices[0])*1.006 < float(self.cryptoPrice) and float(self.cryptoPrice) > float(self.average_cost+float(self.average_cost*float(self.ac_ceiling))):
                    priceCompareSellFlag = True
                    
            elif self.numOfRuns == 4:
                if float(self.historicalPrices[0])*1.005 < float(self.cryptoPrice) and float(self.cryptoPrice) > float(self.average_cost+float(self.average_cost*float(self.ac_ceiling))):
                    priceCompareSellFlag = True
                    
            elif self.numOfRuns == 3:
                if float(self.historicalPrices[0])*1.004 < float(self.cryptoPrice) and float(self.cryptoPrice) > float(self.average_cost+float(self.average_cost*float(self.ac_ceiling))):
                    priceCompareSellFlag = True
                    
            elif self.numOfRuns == 2:
                if float(self.historicalPrices[0])*1.003 < float(self.cryptoPrice) and float(self.cryptoPrice) > float(self.average_cost+float(self.average_cost*float(self.ac_ceiling))):
                    priceCompareSellFlag = True
                    
        #SELL
        if self.numOfRuns >= 7:

            if float(self.cryptoPrice)*0.993 > float(self.historicalPrices[0]) and float(self.cryptoPrice) > float(self.average_cost+float(self.average_cost*float(self.ac_ceiling))):
                priceCompareSellFlag = True
            
            elif float(self.cryptoPrice)*0.994 > float(self.historicalPrices[1]) and float(self.cryptoPrice) > float(self.average_cost+float(self.average_cost*float(self.ac_ceiling))):
                priceCompareSellFlag = True
                
            elif float(self.cryptoPrice)*0.995 > float(self.historicalPrices[2]) and float(self.cryptoPrice) > float(self.average_cost+float(self.average_cost*float(self.ac_ceiling))):
                priceCompareSellFlag = True
                
            elif float(self.cryptoPrice)*0.996 > float(self.historicalPrices[3]) and float(self.cryptoPrice) > float(self.average_cost+float(self.average_cost*float(self.ac_ceiling))):
                priceCompareSellFlag = True
                
            elif float(self.cryptoPrice)*0.997 > float(self.historicalPrices[4]) and float(self.cryptoPrice) > float(self.average_cost+float(self.average_cost*float(self.ac_ceiling))):
                priceCompareSellFlag = True
                
            elif float(self.cryptoPrice)*0.998 > float(self.historicalPrices[5]) and float(self.cryptoPrice) > float(self.average_cost+float(self.average_cost*float(self.ac_ceiling))):
                priceCompareSellFlag = True


        '''
        End of price comparison pecentage change algorithm section
        '''

    def check_sell_flag(self):
        if self.priceCompareSellFlag == True and self.xyz1flag1 == True and self.xyz1flag2 == True and self.xyz1flag5 == True:
            order = robin_stocks.orders.order_sell_crypto_by_price(self.ticker, float(self.shares2sellDollar))
            print(order)
            print("\nsold: ", float(self.cryptoPrice)*0.996)
            print("avg cost:", self.average_cost, "\n")
            updateSharesSell = float(self.shares2sellDollar)/float(float(self.cryptoPrice)*0.996)
            self.num_shares -= updateSharesSell
            
        elif self.priceCompareSellFlag == True and self.xyz1flag15 == True and self.xyz1flag30 == True and self.xyz1flag60 == True and self.xyz1flag120 == True:
            order = robin_stocks.orders.order_sell_crypto_by_price(self.ticker, float(self.shares2sellDollar))
            print(order)
            print("\nsold:", float(self.cryptoPrice)*0.996)
            print("avg cost:", self.average_cost, "\n")
            updateSharesSell = float(self.shares2sellDollar)/float(float(self.cryptoPrice)*0.996)
            self.num_shares -= updateSharesSell
    def check_buy_flag(self):
        if self.priceCompareBuyFlag == True:
            order = robin_stocks.orders.order_buy_crypto_by_price(self.ticker, float(self.shares2buyDollar))
            print(order)
            print("\nbought:", float(self.cryptoPrice)*1.0039)
            newShares = float(float(self.shares2buyDollar)*1.0039)
            tempval = self.average_cost*self.num_shares
            self.average_cost = tempval
            self.average_cost += newShares
            self.updateSharesBuy = float(self.shares2buyDollar)/float(float(self.cryptoPrice)*1.0039)
            self.num_shares += self.updateSharesBuy
            self.average_cost /= float(self.num_shares)
            print("avg cost:", str(self.average_cost), "\n")
                

test = CryptoBot()
test.main_trigger()
