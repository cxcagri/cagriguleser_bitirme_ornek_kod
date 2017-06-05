import cv2
import numpy as np
from threading import Thread
from openalpr import Alpr
import time
import RPi.GPIO as GPIO
from imutils.video import FPS

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(25,GPIO.OUT)


alpr = Alpr("eu", "/home/pi/openalpr/openalpr.conf", "/home/pi/openalpr/runtime_data")#kutuphanenin adresi yazilir


if not alpr.is_loaded():
    print("Error loading OpenALPR")#kutuphane bulunamadiysa hata kodu cikar


alpr.set_top_n(1) #1 adet deneme yapilmaktadir
alpr.set_default_region("eu")#eu kutuphane dosyası tr ozelliklerine gore yeniden duzenlenerek eu ismi verilmistir

camera_index = 0#1 adet kamera kullanilmaktadir
cap = cv2.VideoCapture(camera_index)
cap.set(3,640)
cap.set(4,480)
cap.set(14,75)
time.sleep(2)
cap.set(15,-8.0)
#kamera parametre ayarlari
i = 0
results2 = alpr.recognize_file("/home/pi/plaka3.jpg") #database uzerindeki ornek resim islenmek icin result2 ye atanir
for plate in results2['results']:
    i += 1
        print("Plate #%d" % i)
            print("   %12s %12s" % ("Plate", "Confidence"))
            for candidate2 in plate['candidates']:
                prefix = "-"
                
                
                print("  %s %12s%12f" % (prefix, candidate2['plate'], candidate2['confidence'])) #plaka tahmin orani ile sonucu yazdirilir

while(True):
    
    
    ret, frame = cap.read()#kameradan goruntu okunur
    
    
    if ret:
        
        
        cv2.imwrite("img.jpg", frame)
        
        results1 = alpr.recognize_file("img.jpg")
        
        
        
        for plate in results1['results']:
            i += 1
            print("Plate #%d" % i)
            print("   %12s %12s" % ("Plate", "Confidence"))
            for candidate1 in plate['candidates']:
                prefix = "-"
                
                print("  %s %12s%12f" % (prefix, candidate1['plate'], candidate1['confidence']))
                cap.release()
                camera_index = 0
                cap = cv2.VideoCapture(camera_index)
                cap.set(3,320)
                cap.set(4,240) # her yakalamadan sonra kamera yeniden ayarlanir
                a=candidate1['plate']
                b=candidate2['plate']
                dosya=open("/home/pi/plakalar.txt","a")#kameradan alinan tahminler txt dosyasina yazdirilir
                
                dosya.write(prefix)
                dosya.write(a)
                dosya.close()
                
                
                
                
                
                if a == b: #candidate2['plate']: #database ile kameradan yakalanan plaka uygun ise 25 nolu pin high yapılır
                    print("kapi acildi")
                        GPIO.output(25,GPIO.HIGH)
                            time.sleep(5)
                                GPIO.output(25,GPIO.LOW)
                                    print("kapi kapandi")
    

else:
    break;




# islemler bittiginde , kamerayi birak 
cap.release()
alpr.unload()
cv2.destroyAllWindows()
