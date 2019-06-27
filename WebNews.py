# import required modules 
import requests, json 
import os
from time import sleep

class WebNews():

    def __init__(self):
        pass
   
    def GO(self):
        try:
            file = open("/home/pi/news.key", "r")
            api_key = file.read().rstrip() 
            file.close()

            # base_url variable to store url 
            base_url = "https://newsapi.org/v2/top-headlines?sources=google-news"        
            complete_url = base_url + "&apiKey=" + api_key
            response = requests.get(complete_url)         
            x = response.json()         
            if x["status"] == "ok":   
                art = x["articles"][0:5]
                cmd = '/usr/local/bin/flite -voice slt -t "Number of articles {}"'.format(str(len(art)))
                os.system(cmd)
                sleep(0.5) 
                x = 0
                for val in art:
                    x += 1
                    title = val["title"]
                    #cmd = 'espeak -s 125 -v en+f5 "{}" 2>/dev/null'.format(title)
                    print(title)
                    cmd = '/usr/local/bin/flite -voice slt -t "Article number {}"'.format(str(x))
                    os.system(cmd)             
                    sleep(0.5) 
                    cmd = '/usr/local/bin/flite -voice slt -t "{}"'.format(title)
                    os.system(cmd)
                    sleep(0.5) 
        except:
            pass

if __name__ == "__main__":
    foo = WebNews()
    foo.GO()