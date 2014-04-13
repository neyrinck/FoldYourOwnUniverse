# converts image into 64x64 txt file for use in simulator
import sys

from PIL import Image

im = Image.open('NASA_logo.jpg')
#im.show()
#im.convert('LA').show()
#im.convert('LA').resize((64,64),Image.ANTIALIAS).show()
data = im.convert('LA').resize((64,64),Image.ANTIALIAS)

#scale values from 0 to 1
pixels = list(data.getdata())

elements = []
for pair in pixels:
    value =  float(pair[0])/255
    v =  "%.2f" % value
    elements.append(v)
    

count = 0
for item in elements:
    print item,
    count +=1
    if count % 64 == 0:
        print ' '

