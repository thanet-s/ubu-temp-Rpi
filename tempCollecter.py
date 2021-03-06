import Adafruit_DHT as DHT
import pandas as pd
import datetime
import requests as req
import time

rpiId = 1

print('UBU-TEMP Collecter running')
updateOneData = []

def senddata(data):
    url = 'https://www.ubu-temp.ml/addsensor'
    sendData = req.post(url, data = data)
    return sendData
    
while True:
    time.sleep(1)
    dt = datetime.datetime.now()
    if (dt.minute % 5) == 0 :
        humidity, temperature = DHT.read_retry(11, 8)
        if len(updateOneData) == 0:
            if humidity is not None and temperature is not None:
                updateOneData.append("You must not append anything.")
                data = {
                    'temp': [temperature],
                    'date': [dt.strftime("%Y-%m-%d")],
                    'time': [dt.strftime("%H:%M:%S")],
                }
                try:
                    obj = {
                        'rpiId': rpiId,
                        'temp': data['temp'][0],
                        'date': data['date'][0],
                        'time': data['time'][0]
                    }
                    send = senddata(obj)
                    print(f'Time: {dt.strftime("%H:%M:%S")} send realtime Temp={temperature}*C {send}')        
                except:
                    df = pd.DataFrame(data)
                    df.to_csv('temp.csv', mode='a', index=False, header=False)
                    print(f'Time: {dt.strftime("%H:%M:%S")} Temp={temperature}*C save to csv')
                    
            else:
                print(f'Time: {dt.strftime("%H:%M:%S")}  Sensor fail na kub')              
    else:
        updateOneData.clear()
        try :
            readcsv = open("temp.csv", 'r+').readlines()
            csv2 = list(readcsv)
            nline = len(readcsv)
            if nline == 0:
                pass
            else:
                for i in range(nline):   
                    sensorline = readcsv[i].split(",")
                    obj = {
                        'rpiId': rpiId,
                        'temp': sensorline[0],
                        'date': sensorline[1],
                        'time': sensorline[2][:-1]
                    }
                    send = senddata(obj)
                    print(f'Time: {dt.strftime("%H:%M:%S")} send readcsv time={obj["time"]} Temp={obj["temp"]}*C {send}')  
                    csv2.remove(readcsv[i])
                open("temp.csv",'w').writelines(csv2)
        except Exception as track:
            #print("err", track)
            time.sleep(20)