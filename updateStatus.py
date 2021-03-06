import time
import requests as req

while True:
    try:
        update = req.get('https://www.ubu-temp.ml/update/1')
        print(update)
    except:
        pass
    time.sleep(30)