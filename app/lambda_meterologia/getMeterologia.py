import requests
import json
import logging
import datetime


class Meteroligia:
    def __init__(self):
        self.apiKey='ac89356352059d0b0dceb286beb5e1d9'
        self.url = "http://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}&units=metric"
        
    def request(self, cidade):
        url = self.url.format(cidade,self.apiKey)
        
        try:
           r = requests.get(url)
        except requests.ConnectionError as e:
           logging.error(e)
           r = {'cod' : 500, 'message': e }
        return(r.json())
        
    def format(self, request):
        data = datetime.datetime.now()
        package = {
            "name": request['name'],
            "data": data.strftime("%d-%m-%Y"),
            "temp_max" : request['main']['temp_max'],
            "temp_min" : request['main']['temp_min'],
            "coord": {
               "lat": request['coord']['lat'],
               "lon": request['coord']['lon']
             },
        }
        
        return package
    def get(self,cidade):
        request =  self.request(cidade)

        if request['cod'] == 200:
           request = self.format(request)
        
        return request   
        


cidade="sao paulo"

x=Meteroligia()
k = x.get(cidade)
print(k)




    
    
    
