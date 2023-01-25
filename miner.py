from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import time
import numpy as np
from datetime import datetime, timedelta
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--day", dest="day", help="Day Value")
parser.add_argument("-m", "--month", dest="month", help="Month Value")
parser.add_argument("-y", "--year", dest="year", help="Year Value")
parser.add_argument("-u", "--utc", dest="time", help="Time Value")
parser.add_argument("-t", "--type", dest="type", help="1 for Wind Speed, Direction and Relative Humidity \n 2 for Current Speed, Direction and Temperature")

options = parser.parse_args()

#utc = ["0000","0600","1200","1800"]
utc = [str(options.time)]

start = datetime(int(options.year), int(options.month), int(options.day))
end = start+timedelta(days=1)

try:
    if(str(options.type)=="1"):
        while(start!=end):
            stringdate = start.strftime('%Y-%m-%d')
            start = start + timedelta(days=1)
            filename = stringdate.replace("-", "_")
            htmldate = stringdate.replace("-", "/")

            for l in utc:
                reset = 1
                driver = webdriver.Firefox()
                driver.get("https://earth.nullschool.net/#"+htmldate+"/"+l+"Z/wind/surface/level/overlay=relative_humidity/loc=0,0")
                time.sleep(4)
                counter=1
                stringdir=""
                stringspeed=""
                stringrelativehumidity=""
                print(htmldate+"_"+l)
                for i in np.arange(30.00,-10.20,-0.20):
                    i = round(i, 1)

                    if (reset == 50):
                        driver.close()
                        driver = webdriver.Firefox()
                        driver.get("https://earth.nullschool.net/#"+htmldate+"/"+l+"Z/wind/surface/currents/overlay=temp/loc=0,0")
                        time.sleep(4)
                        reset=1

                    for j in np.arange(60.00,100.20,0.20):
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
                    
                    reset+=1

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

    if(str(options.type)=="2"):
        while(start!=end):
            stringdate = start.strftime('%Y-%m-%d')
            start = start + timedelta(days=1)
            filename = stringdate.replace("-", "_")
            htmldate = stringdate.replace("-", "/")

            for l in utc:
                reset = 1
                driver = webdriver.Firefox()
                driver.get("https://earth.nullschool.net/#"+htmldate+"/"+l+"Z/wind/surface/currents/overlay=temp/loc=0,0")
                time.sleep(4)
                counter=1
                stringdir=""
                stringspeed=""
                stringtemperature=""
                print(htmldate+"_"+l)
                for i in np.arange(30.00,-10.20,-0.20):
                    i = round(i, 1)

                    if (reset == 50):
                        driver.close()
                        driver = webdriver.Firefox()
                        driver.get("https://earth.nullschool.net/#"+htmldate+"/"+l+"Z/wind/surface/currents/overlay=temp/loc=0,0")
                        time.sleep(4)
                        reset=1

                    for j in np.arange(60.00,100.20,0.20):
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
                    
                    reset+=1

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
except:
    try:
        driver.close()
    except:
        exit(1)
    exit(1)
else:
    exit(0)
