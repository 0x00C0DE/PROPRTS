import matplotlib.pyplot as plt
from scipy import stats
import sys
import os

class createLRmodel():
    y = []
    yy = []
    x = []
    xx = []
    slope = 0
    intercept = 0
    def read_lr_data(self):
        # Using readlines()
        dataFile = sys.argv[1]
        file1 = open(dataFile, 'r')
        Lines = file1.readlines()
        numLines = len(Lines)
        #print("numlines: ", numLines)
        # Strips the newline character
        for line in Lines:
            if line == "\n":
                break
            line = line.replace('(','').replace(')','')
            line = line.replace(',', '')
            line = line.split()
            #print("line[0]: ", line[0])
            #print("line[1]: ", line[1])
            self.xx.append(line[0])
            self.xx = [float(i) for i in self.xx]
            self.yy.append(line[1])
            self.yy = [float(i) for i in self.yy]
        file1.close()
        self.x.clear()
        self.y.clear()
        self.x = [float(i) for i in self.xx]
        self.y = [float(i) for i in self.yy]
        self.xx.clear()
        self.yy.clear()

        self.slope, self.intercept, r, p, std_err = stats.linregress(self.x, self.y)

        mymodel = list(map(self.myfunc, self.x))

        plt.clf()
        plt.scatter(self.x, self.y)
        plt.plot(self.x, mymodel)
        plt.title("PROPRTS-1-LinearRegression")
        plt.savefig("PROPRTS-1-LR.png")

    def myfunc(self, x):
      return self.slope * x + self.intercept

    def is_txt_file(self, filename):
        _, ext = os.path.splitext(filename)
        return ext == '.txt'

if len(sys.argv) == 1:
    print("[ERROR]")
    print("not enough args.lol: ", len(sys.argv))
else:
    #print("arg 3: ", sys.argv[1])
    #print("arg length: ", len(sys.argv))
    test = createLRmodel()
    if test.is_txt_file(sys.argv[1]) == True:
        test.read_lr_data()
    elif len(sys.argv) > 2:
        print("too many data files, only 1 allowed")
    else:
        print("There are no data files to load [ERROR]")


