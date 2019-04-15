# import required modules 
import requests, json 
import os

class WebWeather():

    def __init__(self):
        pass

    def K2F(self, k): 
        d = ( k- 273.15 ) * 9 / 5 + 32;
        return round(d,0)
    
    def GO(self):
        try:
            file = open("/home/pi/weather.key", "r")
            api_key = file.read().rstrip() 
            file.close()

            # base_url variable to store url 
            base_url = "http://api.openweathermap.org/data/2.5/weather?"        
            complete_url = base_url + "appid=" + api_key + "&zip=21502,US"
            response = requests.get(complete_url)         
            x = response.json()         
            if x["cod"] != "404":   
                y = x["main"]         
                current_temperature = self.K2F(y["temp"])            
                weather_description = x["weather"][0]["description"] 
                cmd = 'flite -voice slt -t "The current temperature is {} fahrenheit and the weather outside is {}"'.format(current_temperature, weather_description)
                os.system(cmd)
        except:
            pass

if __name__ == "__main__":
    foo = WebWeather()
    foo.GO()