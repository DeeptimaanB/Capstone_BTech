from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import time
import numpy as np
from datetime import datetime, timedelta
import string




#utc = ["0000","0300","0600","0900","1200","1500","1800","2100"]
utc = ["1200","1500","1800","2100"]

start = datetime(2015, 1, 6)
end = datetime(2015, 1, 7)


while(start!=end):
    stringdate = start.strftime('%Y-%m-%d')
    start = start + timedelta(days=1)
    filename = stringdate.replace("-", "_")
    htmldate = stringdate.replace("-", "/")

    for l in utc:
        driver = webdriver.Firefox()
        driver.get("https://earth.nullschool.net/#"+htmldate+"/"+l+"Z/wind/surface/level/overlay=relative_humidity/loc=0,0")
        time.sleep(4)
        counter=1
        stringdir=""
        stringspeed=""
        stringrelativehumidity=""
        print(htmldate+"_"+l)
        for i in np.arange(30.00,-10.10,-0.10):
            i = round(i, 1)
            
            for j in np.arange(60.00,100.10,0.10):
                j = round(j, 1)
                site="https://earth.nullschool.net/#"+htmldate+"/"+l+"Z/wind/surface/level/overlay=relative_humidity/loc="+str(j)+","+str(i) 
                driver.get(site)
                coord = driver.find_element(By.XPATH, "//div[@id='spotlight-panel']/div[1]/div[1]")
                spotlight = driver.find_element(By.XPATH, "//div[@id='spotlight-panel']/div[2]/div[1]")
                humidity = driver.find_element(By.XPATH, "//div[@id='spotlight-panel']/div[3]/div[1]")
                pattern = r'[^A-Za-z0-9.]+'
                x = spotlight.text.split("@")
                angle = re.sub(pattern, '', x[0])
                speed = re.sub(pattern, '', x[1])
                
                rh = re.sub(pattern, '', humidity.text)
                stringdir = stringdir+angle+","
                stringspeed=stringspeed+speed+","
                stringrelativehumidity=stringrelativehumidity+rh+","

            stringdir = stringdir+angle+"\n"
            stringspeed=stringspeed+speed+"\n"
            stringrelativehumidity=stringrelativehumidity+rh+"\n"
            
            print(counter)
            counter+=1
        driver.close()
        f = open("rh/rh_"+filename+"_"+l+".csv", "w")
        f.write(stringrelativehumidity)
        f.close()

        f = open("wind_direction/w_d_"+filename+"_"+l+".csv", "w")
        f.write(stringdir)
        f.close()

        f = open("wind_speed/w_s_"+filename+"_"+l+".csv", "w")
        f.write(stringspeed)
        f.close()


