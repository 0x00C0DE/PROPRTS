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
import subprocess
from datetime import datetime, timedelta
import random

script_path = "E:/Downloads/PROPRTS/proprtsImageViewer-1-protoV1.py"

totp = pyotp.TOTP("Sauce").now()
login = robin_stocks.login("email_here@test.com", "password_here")

# Scheduler created to run every 15 minutes
s = sched.scheduler(time.time, time.sleep)

# 10 second interval price history list, for every 1 minute
historicalPrices = []
reorderArray = []

# keeps track of the number of runs since the start of the program
numOfRuns = 1.0

y = []
x = []

tempcounter = 1
tempcounter2 = 1
priceCompareBuyFlag = False
priceCompareSellFlag = False
cryptoPrice = 0
def run(sc):

    # crypto currency ticker available on robinhood
    ticker = "MATIC"

    global priceCompareBuyFlag
    global priceCompareSellFlag
    global historicalPrices 
    global reorderArray

    global ac_ceiling
    global ac_floor
    global updateSharesSell
    global updateSharesBuy
    
    global Shares2Sell
    global Shares2Buy
    global numOfRuns
    global average_cost
    global num_shares
    global cryptoPrice
    
    cryptoSymbol = robin_stocks.crypto.get_crypto_quote(ticker, info="mark_price")
    cryptoPrice = float(cryptoSymbol)
    print(ticker + ": $" + str(cryptoSymbol))

    '''
    Beginning of linear regression section
    '''
    global tempcounter
    global tempcounter2
    global y
    global x
    global slope
    global intercept
    global r
    global p
    global std_err
    
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    x.append(ts)
    y.append(cryptoPrice)
    slope, intercept, r, p, std_err = stats.linregress(x, y)

    if (len(x) >= 97):
        x = x[1:96]

    if (len(y) >= 97):
        y = y[1:96]
    coordinate =list(zip(x,y))

    if (len(coordinate)) > 96:
        tempCoord = coordinate[1:97]
        coordinate = coordinate[-1:]
        coordinate = tempCoord + coordinate

    if (len(coordinate)) >= 96:
        file_clear = open("PROPRTS-1-LR-data.txt", "w")
        file_clear.close()
        for element in coordinate:
            file1 = open("PROPRTS-1-LR-data.txt","a")
            file1.write(f"{element} \n")
            file1.close()
            print("done, writing new data to txt file")
            
    mymodel = list(map(myfunc, x))
    pricer = myfunc(tempcounter)
    tempcounter += 1
    predictionMinutesAhead = dt + timedelta(minutes = 120)
    pts = datetime.timestamp(predictionMinutesAhead)
    price = myfunc(pts)
    print("\nprice prediction", ((pts-ts)/60), "minutes ahead from now:$", price, " [ " , predictionMinutesAhead , " ] ")
    predictionMinutesAhead2 = dt + timedelta(minutes = 60)
    pts2 = datetime.timestamp(predictionMinutesAhead2)
    price2 = myfunc(pts2)
    print("price prediction", ((pts2-ts)/60), "minutes ahead from now:$", price2, " [ " , predictionMinutesAhead2 , " ] ")
    predictionMinutesAhead3 = dt + timedelta(minutes = 30)
    pts3 = datetime.timestamp(predictionMinutesAhead3)
    price3 = myfunc(pts3)
    print("price prediction", ((pts3-ts)/60), "minutes ahead from now:$", price3, " [ " , predictionMinutesAhead3 , " ] ")
    predictionMinutesAhead4 = dt + timedelta(minutes = 15)
    pts4 = datetime.timestamp(predictionMinutesAhead4)
    price4 = myfunc(pts4)
    print("price prediction", ((pts4-ts)/60), "minutes ahead from now:$", price4, " [ " , predictionMinutesAhead4 , " ] ")
    predictionMinutesAhead5 = dt + timedelta(minutes = 5)
    pts5 = datetime.timestamp(predictionMinutesAhead5)
    price5 = myfunc(pts5)
    print("price prediction", ((pts5-ts)/60), "minutes ahead from now:$", price5, " [ " , predictionMinutesAhead5 , " ] ")
    predictionMinutesAhead6 = dt + timedelta(minutes = 2)
    pts6 = datetime.timestamp(predictionMinutesAhead6)
    price6 = myfunc(pts6)
    print("price prediction", ((pts6-ts)/60), "minutes ahead from now:$", price6, " [ " , predictionMinutesAhead6 , " ] ")
    predictionMinutesAhead7 = dt + timedelta(minutes = 1)
    pts7 = datetime.timestamp(predictionMinutesAhead7)
    price7 = myfunc(pts7)
    print("price prediction", ((pts7-ts)/60), "minutes ahead from now:$", price7, " [ " , predictionMinutesAhead7 , " ] ", "\n")

    print("current time: ", dt, "\n")
    # Keeps track of counter
    
    print("\n numOfRuns PROPRTS-1: " + str(numOfRuns) + "\n")
    numOfRuns += 1
    
    print("slope:", slope)
    print("intercept:", intercept)
    print("r:", r)
    print("p:", p)
    print("std_err:", std_err)
    
    plt.clf()
    plt.scatter(x, y)
    plt.plot(x, mymodel)
    plt.title("PROPRTS-1")
    plt.savefig("LR1-proto-V1.png")

    '''
    End of linear regression section
    '''
    # calls scheduler every 1 minutes
    s.enter(60, 1, run, (sc,))
    
def myfunc(x):
    return slope * x + intercept

def convertTuple(tup):
    " ".join(str(x) for x in tup)

subprocess.Popen(["python", "-i", script_path], start_new_session=True)

s.enter(1, 1, run, (s,))
s.run()
