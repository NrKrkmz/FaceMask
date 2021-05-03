#!/usr/bin/env python
from __future__ import print_function
import cv2 
import numpy as np 
import matplotlib.pyplot as plt
import sys 
from common import Sketcher
 
 
# Kullanacağımız resmi tanımlayalım
INPUT_IMAGE = "human2.jpg"
IMAGE_NAME = INPUT_IMAGE[:INPUT_IMAGE.index(".")]
OUTPUT_IMAGE = IMAGE_NAME + "_output.jpg"
TABLE_IMAGE = IMAGE_NAME + "_table.jpg"
 
def main():
    try:
        fn = sys.argv[1]
    except:
        fn = INPUT_IMAGE
 
    image = cv2.imread(cv2.samples.findFile(fn))
  
    # Resim bulunamazsa program bozulmasın
    if image is None:
        print('Failed to load image file:', fn)
        sys.exit(1)
 
    # Common dosyamızdan örnek oluşturalım
    image_mark = image.copy()
    sketch = Sketcher('Image', [image_mark], lambda : ((255, 255, 255), 255))
 
    # Kullanıcı Komut alanı
    while True:
        ch = cv2.waitKey()
        if ch == 27: # ESC - exit
            break
        if ch == ord('r'): # r - mask the image
            break
        if ch == ord(' '): # SPACE - reset the inpainting mask
            image_mark[:] = image
            sketch.show()
 
    # Ten rengine göre uygun renk aralığı ataması
    lower_white = np.array([50,50,50])
    upper_white = np.array([255, 255, 255])
 
    mask = cv2.inRange(image_mark, lower_white, upper_white)
 
    # Maskeleme işlemi
    mask_inv = cv2.bitwise_not(mask)
 
    # Renk dönüşüm alanı
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
    
    rows, cols, channels = image.shape
    image = image[0:rows, 0:cols]
 
    colored_portion = cv2.bitwise_or(image, image, mask = mask)
    colored_portion = colored_portion[0:rows, 0:cols]
 
    gray_portion = cv2.bitwise_or(gray, gray, mask = mask_inv)
    gray_portion = np.stack((gray_portion,)*3, axis=-1)
 
    # Çıktı oluşturulan alan
    output = colored_portion + gray_portion
 
    # Çıktıyı kayıt edelim
    cv2.imwrite(OUTPUT_IMAGE, output)
 
    # Fotoğrafın ilk ve son halini tabloya dönüştürelim
    mask = np.stack((mask,)*3, axis=-1)
    table_of_images = np.concatenate((image, mask), axis=1)
    cv2.imwrite(TABLE_IMAGE, table_of_images)
 
    # Kullanıcıya gösterelim
    #cv2.imshow('Original Image', image)
    #cv2.imshow('Output Image', output)
    cv2.imshow('Table of Images', table_of_images)
    cv2.waitKey(0) 
 
if __name__ == '__main__':
    print(__doc__)
    main()
    cv2.destroyAllWindows()