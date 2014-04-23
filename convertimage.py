# converts image into 64x64 txt file for use in simulator
import sys
from PIL import Image

if len(sys.argv) != 2:
    print 'Usage:'
    print 'python convertimage.py NASA_logo.jpg'
else:
    im = Image.open(sys.argv[1])
    #im.show()
    #im.convert('LA').show()
    #im.convert('LA').resize((64,64),Image.ANTIALIAS).show()
    data = im.convert('LA').resize((64,64),Image.ANTIALIAS)

    pixels = list(data.getdata())

    elements = []
    for pair in pixels:
        value =  float(pair[0])/255
        v =  "%.2f" % value
        #elements.append(v)
        elements.insert(0, v)
    
    #rev = elements[::-1]
    count = 0
    for item in elements:
        print item,
        count += 1
        if count % 64 == 0:
            print ' '

    #printed output can be redirected to file, e.g. densmesh4.txt:
    #python convertimage.py newimage.jpg > densmesh4.txt
