import cv2
import sys
import urllib.request

# Download the image from GitHub
url = 'https://raw.githubusercontent.com/0x00C0DE/PROPRTS/main/src/proprts/PROPRTS-1-LR.png'
urllib.request.urlretrieve(url, 'PROPRTS-1-LR.png')

while True:
    try:
        image1 = cv2.imread("PROPRTS-1-LR.png")
        cv2.imshow("Window", image1)
        cv2.waitKey(9000)
        cv2.destroyAllWindows()
    except:
        pass
