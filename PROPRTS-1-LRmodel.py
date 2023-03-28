import matplotlib.pyplot as plt
from scipy import stats

dataFile = 'PROPRTS-1-data.txt'

# Using readlines()
file1 = open(dataFile, 'r')
Lines = file1.readlines()

y = []
yy = []
x = []
xx = []

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
x = [float(i) for i in xx]
y = [float(i) for i in yy]
xx.clear()
yy.clear()

slope, intercept, r, p, std_err = stats.linregress(x, y)

def myfunc(x):
  return slope * x + intercept

mymodel = list(map(myfunc, x))

plt.clf()
plt.scatter(x, y)
plt.plot(x, mymodel)
plt.title("PROPRTS-1-LinearRegression")
plt.savefig("PROPRTS-1-LR.png")
