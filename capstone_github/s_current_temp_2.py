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
        driver.get("https://earth.nullschool.net/#"+htmldate+"/"+l+"Z/wind/surface/currents/overlay=temp/loc=0,0")
        time.sleep(4)
        counter=1
        stringdir=""
        stringspeed=""
        stringtemperature=""
        print(htmldate+"_"+l)
        for i in np.arange(30.00,-10.10,-0.10):
            i = round(i, 1)
            
            for j in np.arange(60.00,100.10,0.10):
                j = round(j, 1)
                site="https://earth.nullschool.net/#"+htmldate+"/"+l+"Z/wind/surface/currents/overlay=temp/loc="+str(j)+","+str(i) 
                driver.get(site)
                spotlight = driver.find_element(By.XPATH, "//div[@id='spotlight-panel']/div[2]/div[1]")
                temp = driver.find_element(By.XPATH, "//div[@id='spotlight-panel']/div[3]/div[1]")
                pattern = r'[^A-Za-z0-9.]+'
                tpattern = r'[^A-Za-z0-9.-]+'
                if (len(spotlight.text) == 0):
                    angle = "0"
                    speed = "0"
                else:
                    x = spotlight.text.split("@")
                    angle = re.sub(pattern, '', x[0])
                    speed = re.sub(pattern, '', x[1])

                t = re.sub(tpattern, '', temp.text)

                stringdir = stringdir+angle+","
                stringspeed=stringspeed+speed+","
                stringtemperature=stringtemperature+t+","

            stringdir = stringdir+angle+"\n"
            stringspeed=stringspeed+speed+"\n"
            stringtemperature=stringtemperature+t+"\n"
            
            print(counter)
            counter+=1
        
        driver.close()
        f = open("temp/t_"+filename+"_"+l+".csv", "w")
        f.write(stringtemperature)
        f.close()

        f = open("current_direction/c_d_"+filename+"_"+l+".csv", "w")
        f.write(stringdir)
        f.close()

        f = open("current_speed/c_s_"+filename+"_"+l+".csv", "w")
        f.write(stringspeed)
        f.close()


