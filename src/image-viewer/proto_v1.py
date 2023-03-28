
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import ion
import time
import sched
from PIL import Image
import cv2
import subprocess
from threading import *


s = sched.scheduler(time.time, time.sleep)

def run(sc):
    while True:
        try:
            image1 = cv2.imread("E:\\Downloads\\PROPRTS\\LR1-protoV1.png")
            cv2.imshow("Window", image1)
            cv2.waitKey(9000)
            cv2.destroyAllWindows()
            s.enter(1, 1, run, (sc,))
        except:
            pass

s.enter(1, 1, run, (s,))
s.run()

