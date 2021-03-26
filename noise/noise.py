import numpy as np
import os
from PIL import Image
from random import random, randint
import glob

IMG_WIDTH = 256
IMG_HEIGHT = IMG_WIDTH
A = 20
f = 0
imgNum = 0


def emptyImg():
    eImg = []
    for row in range(IMG_HEIGHT):
        for pixel in range(IMG_WIDTH):
            eImg.append([0, 0, 0])
    generateImage(eImg)


def bwAlpha():
    img = list()
    for row in range(IMG_HEIGHT):
        for pixel in range(IMG_WIDTH):
            ri = randint(0, 255)
            if random() < 0.5:
                newPixel = [255, 0, ri]
            else:
                newPixel = [0, 255, ri]

            img.append(newPixel)
            # if row == 0:
            # generateImage(img)
    generateImage(img)
    return img


def beaching(img):
    for pixel in range(len(img)):

        p = 0
        if (pixel - (IMG_WIDTH - 1)) < 0:
            p += 1 if random() < 0.15 else 0
        else:
            p += 1 if (img[pixel][0] != img[pixel - 1][0]) else 0
            p += 1 if (img[pixel][0] != img[pixel - IMG_WIDTH][0]) else 0
            p += 1 if (img[pixel][0] != img[pixel - IMG_WIDTH - 1][0]) else 0
            p += 1 if (img[pixel][0] != img[pixel - IMG_WIDTH + 1][0]) else 0
        if (pixel + (IMG_WIDTH + 1)) < len(img):
            p += 1 if (img[pixel][0] != img[pixel + 1][0]) else 0
            p += 1 if (img[pixel][0] != img[pixel + IMG_WIDTH][0]) else 0
            p += 1 if (img[pixel][0] != img[pixel + IMG_WIDTH - 1][0]) else 0
            p += 1 if (img[pixel][0] != img[pixel + IMG_WIDTH + 1][0]) else 0
        else:
            p += 1 if random() < 0.15 else 0
        if p >= 1:
            img[pixel][2] = 1

        generateImage(img)
    return img


def smoothAlpha(img, times=4):
    for time in range(times):

        newImg = list()
        for pixel in range(len(img)):

            p, lp, rp, tp, bp = 1, 0, 0, 0, 0

            # left pixel value
            if pixel % IMG_WIDTH != 0:
                lp = img[pixel - 1][2]
                p += 1

            # right pixel value
            if (pixel + 1) % IMG_WIDTH != 0:
                rp = img[pixel + 1][2]
                p += 1

            # top pixel value
            if (pixel - IMG_WIDTH) > (-1):
                tp = img[pixel - IMG_WIDTH][2]
                p += 1

            # bottom pixel value
            if pixel + IMG_WIDTH < len(img):
                bp = img[pixel + IMG_WIDTH][2]
                p += 1

            if img[pixel][0] == 255:
                alpha = ((img[pixel][2]
                          + lp
                          + rp
                          + tp
                          + bp) / p)
                if (alpha - A) <= 0:
                    alpha = 1
                img[pixel] = [255, 0, alpha]
            elif img[pixel][0] == 0:
                alpha = ((img[pixel][2]
                          + lp
                          + rp
                          + tp
                          + bp) / p)
                if (alpha - A) <= 0:
                    alpha = 1
                img[pixel] = [0, 255, alpha]

            generateImage(img)
        img = rotateImgArr(img)

    return img


def deScatter(img, times=4):
    for time in range(times):
        for pixel in range(len(img)):

            p = 0
            if (pixel - (IMG_WIDTH - 1)) < 0:
                p += randint(0, 4)
            else:
                p += 1 if (img[pixel][0] != img[pixel - 1][0]) else 0
                p += 1 if (img[pixel][0] != img[pixel - IMG_WIDTH][0]) else 0
                p += 1 if (img[pixel][0] != img[pixel - IMG_WIDTH - 1][0]) else 0
                p += 1 if (img[pixel][0] != img[pixel - IMG_WIDTH + 1][0]) else 0
            if (pixel + (IMG_WIDTH + 1)) < len(img):
                p += 1 if (img[pixel][0] != img[pixel + 1][0]) else 0
                p += 1 if (img[pixel][0] != img[pixel + IMG_WIDTH][0]) else 0
                p += 1 if (img[pixel][0] != img[pixel + IMG_WIDTH - 1][0]) else 0
                p += 1 if (img[pixel][0] != img[pixel + IMG_WIDTH + 1][0]) else 0
            else:
                p += randint(0, 4)

            if p >= 5:
                if img[pixel][0] == 0:
                    img[pixel][0] = 255
                    img[pixel][1] = 0
                elif img[pixel][0] == 255:
                    img[pixel][0] = 0
                    img[pixel][1] = 255

            generateImage(img)
        img = rotateImgArr(img)

    return img


def rotateImgArr(imgArr, debug=True):
    if debug:
        rotImg = list()
        for n in range(IMG_HEIGHT):
            rotImg.append(imgArr[IMG_WIDTH - n - 1::IMG_WIDTH])
        imgArr = [item for l in rotImg for item in l]
    return imgArr


def colorize(img):
    for pixel in range(len(img)):
        if img[pixel][0] == 255 and img[pixel][2] >= 110:
            img[pixel] = [39, 71, 144]
        elif img[pixel][0] == 255 and img[pixel][2] >= 45:
            img[pixel] = [56, 132, 207]
        elif img[pixel][0] == 255 and img[pixel][2] >= 0:
            img[pixel] = [15, 212, 203]
        elif img[pixel][0] == 0 and img[pixel][2] <= 10:
            img[pixel] = [183, 192, 165]
        elif img[pixel][0] == 0 and img[pixel][2] <= 50:
            img[pixel] = [223, 210, 193]
        elif img[pixel][0] == 0 and img[pixel][2] <= 70:
            img[pixel] = [100, 152, 79]
        elif img[pixel][0] == 0 and img[pixel][2] <= 90:
            img[pixel] = [0, 77, 26]
        elif img[pixel][0] == 0 and img[pixel][2] <= 110:
            img[pixel] = [145, 82, 61]
        elif img[pixel][0] == 0 and img[pixel][2] <= 130:
            img[pixel] = [128, 42, 0]
        elif img[pixel][0] == 0 and img[pixel][2] <= 150:
            img[pixel] = [51, 26, 0]
        elif img[pixel][0] == 0 and img[pixel][2] <= 170:
            img[pixel] = [40, 20, 0]
        else:
            img[pixel] = [0, 0, 0]

        generateImage(img)

    return img


def biggerIslands(img, times=1):
    for time in range(times):
        for pixel in range(len(img)):

            p = 0
            if (pixel - (IMG_WIDTH - 1)) < 0:
                p += 1 if random() < 0.15 else 0
            else:
                p += 1 if (img[pixel][0] != img[pixel - 1][0]) else 0
                p += 1 if (img[pixel][0] != img[pixel - IMG_WIDTH][0]) else 0
                p += 1 if (img[pixel][0] != img[pixel - IMG_WIDTH - 1][0]) else 0
                p += 1 if (img[pixel][0] != img[pixel - IMG_WIDTH + 1][0]) else 0
            if (pixel + (IMG_WIDTH + 1)) < len(img):
                p += 1 if (img[pixel][0] != img[pixel + 1][0]) else 0
                p += 1 if (img[pixel][0] != img[pixel + IMG_WIDTH][0]) else 0
                p += 1 if (img[pixel][0] != img[pixel + IMG_WIDTH - 1][0]) else 0
                p += 1 if (img[pixel][0] != img[pixel + IMG_WIDTH + 1][0]) else 0
            else:
                p += 1 if random() < 0.15 else 0
            if p >= 5:
                img[pixel][0] = 254
                img[pixel][1] = 254

            generateImage(img)

    for pixel in range(len(img)):
        if img[pixel][0] == 254:
            img[pixel][0] = 0
            img[pixel][1] = 255
    return img


def generateImage(img, fin=False, debug=False, debugFIN=False):
    global f
    global imgNum
    f += 1
    if f % IMG_WIDTH == 0 or f < IMG_WIDTH or fin or debug:
        if debugFIN:
            new = []
            for i in range(0, len(img), IMG_WIDTH):
                new.append(img[i: i + IMG_WIDTH])
            imgNum += 1
            array = np.asarray(new)
            array = array.astype(np.uint8)
            new = Image.fromarray(array)

            new.save(f"noiseGIF/noise_{'0' * (4 - len(str(imgNum)))}{imgNum}.png")
            new.save("noiselive.png")

            return new


def makeGif():
    fp_in = "noiseGIF/noise_*.png"
    fp_out = "noise.gif"

    img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
    img.save(fp=fp_out, format='GIF', version='GIF89a', append_images=imgs,
             save_all=True, duration=100, loop=0)


def clearFolder():
    files = glob.glob('noiseGIF/*')
    for f in files:
        os.remove(f)


if __name__ == "__main__":
    emptyImg()
    print("empty image created")
    img = bwAlpha()
    print("random sheet created")
    img = deScatter(img, times=4)
    print("descattering done")
    """img = biggerIslands(img)
    print("biggered islands")"""
    img = beaching(img)
    print("beaching done")
    img = smoothAlpha(img)
    print("smoothed alpha")
    img = colorize(img)
    print("colorized")
    try:
        makeGif()
    except:
        pass
    print("gif generated")
    img = generateImage(img, fin=True, debugFIN=True)
    img.save("noiseFIN.png")
    print("success!")
    clearFolder()
    print("noiseGIF folder cleared")
