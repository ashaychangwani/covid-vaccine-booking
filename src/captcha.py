import json
from hashlib import sha256
from collections import Counter
from inputimeout import inputimeout, TimeoutOccurred
import tabulate, copy, time, datetime, requests, sys, os, random
from cairosvg import svg2png
from PIL import Image, ImageEnhance
from io import BytesIO
import requests
import numpy as np
import re
import cv2
import pytesseract


def captcha_buider(resp):
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPM
    from PIL import Image

    with open('captcha.svg', 'w') as f:
        f.write(resp['captcha'])

    drawing = svg2rlg('captcha.svg')
    renderPM.drawToFile(drawing, "captcha.png", fmt="PNG")

    img = Image.open('captcha.png')
    img.show()

def captcha_solver(resp):
    captcha_cleaned = re.sub('(<path d=)(.*?)(fill=\"none\"/>)', '', resp['captcha'])
    png = svg2png(bytestring=captcha_cleaned, scale=3, dpi=500)
    inputimage = Image.open(BytesIO(png)).convert('RGBA')
    enhancer = ImageEnhance.Contrast(inputimage)
    factor = 0.1  # increase contrast
    inputimage = enhancer.enhance(factor)
    image = Image.new("RGB", inputimage.size, "WHITE")
    image.paste(inputimage, (0, 0), inputimage)
    image.save('image_out.png')

    img = cv2.imread('image_out.png')
    text = pytesseract.image_to_string(img, lang='comic')
    text = re.sub(r"[\n\t\s]", "", text)
    print("SOLVED CAPTCHA = ")
    print(text)
    return text

# with open('download.svg','rb') as f:
#     response = f.read()
#     captcha_solver({'captcha':response.decode('utf-8')})