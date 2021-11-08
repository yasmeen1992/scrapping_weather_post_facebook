   
import config
import requests
from bs4 import BeautifulSoup as bs
from PIL import Image, ImageFont, ImageDraw
import arabic_reshaper
from bidi.algorithm import get_display
import datetime
USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
#LANGUAGE = "en-US,en;q=0.5"
LANGUAGE = "en-gb"
########################################################################################
weekDayIndex={'Saturday':0,'Sunday':1,'Monday':2,'Thursday':3,'Wednesday':4,'Tuesday':5,'Friday':6}
coordinate = {
 'Mansoura':{'tempToday':(240,74),'cityName':(240,45),'weatherStatus':(240,100),'todayDate':(240,13),'dayMonth':(350,13)}
 ,'Cairo':{'cityName':(240,170),'tempToday':(240,201),'weatherStatus':(240,230),'todayDate':(240,141),'dayMonth':(350,141)}
 ,'Alexandria':{'cityName':(40,46),'tempToday':(40,73),'weatherStatus':(40,100),'todayDate':(36,13),'dayMonth':(150,13)}
 ,'Aswan':{'cityName':(40,170),'tempToday':(40,201),'weatherStatus':(40,230),'todayDate':(39,141),'dayMonth':(150,141)}
}
####################################################################################
lstCities=['Mansoura','Cairo','Alexandria','Aswan']
citiesWeather={}
def scrape():
    lstWeatherCities=[]
    currentDay = datetime.datetime.now().day
    currentMonth = datetime.datetime.now().strftime('%b')
    for city in lstCities: 
        citiesWeather={}    
        URL = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"
        URL += city
        data = get_weather_data(URL)
        #region=data.find("div", attrs={"id": "wob_loc"}).text
        tempToday=data.find('span',{'id':'wob_tm'}).text+'°C'
        todayDate=data.find("div", attrs={"id": "wob_dts"}).text
        weatherStatus=data.find('span',{'id':'wob_dc'}).text
        citiesWeather[city]={'tempToday':tempToday,'todayDate':todayDate,'weatherStatus':weatherStatus,'dayMonth':str(currentMonth)+'.'+str(currentDay)}
        lstWeatherCities.append(citiesWeather) 
     
    return lstWeatherCities

 
############################################################################################

def post(lstWeatherCities):
    my_image = Image.open("imagesFolder/template.jpg")
    image_editable = ImageDraw.Draw(my_image)
    for itemWeather in lstWeatherCities:
        cityName = list(itemWeather.keys())[0]
        tempToday=itemWeather[cityName]['tempToday']
        weatherStatus=itemWeather[cityName]['weatherStatus']
        todayDate=itemWeather[cityName]['todayDate']
        dayMonth=itemWeather[cityName]['dayMonth']
        blue = (40, 47, 79)
        fontSize=18
        titleFont = ImageFont.truetype('COOPBL.TTF',  fontSize)
        weatherStatusFont=ImageFont.truetype('BAUHS93.TTF',  fontSize-5)
        if cityName in coordinate:
           image_editable.text(coordinate[cityName]['cityName'], cityName, blue, font=titleFont)
           image_editable.text(coordinate[cityName]['tempToday'], tempToday, blue, font=titleFont)
           image_editable.text(coordinate[cityName]['weatherStatus'], weatherStatus, blue, font=weatherStatusFont)
           image_editable.text(coordinate[cityName]['todayDate'], todayDate, blue, font=weatherStatusFont)
           image_editable.text(coordinate[cityName]['dayMonth'], dayMonth, blue, font=weatherStatusFont)
    my_image.save("imagesFolder/result.jpg")
    image_url = 'https://graph.facebook.com/{}/photos'.format(config.page_id_1)
    img_payload = {
        'access_token': config.facebook_access_token_1
    }
    files = {
        'file': open('imagesFolder/result.jpg', 'rb')
    }
    r = requests.post(image_url, data=img_payload, files=files)
##############################################################################################

def get_weather_data(url):
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    session.headers['lang'] = LANGUAGE
    html = session.get(url)
    # create a new soup
    soup = bs(html.text, "html.parser")
    return soup
def adjust_arabic_text(arabic_text):
    reshaped_text = arabic_reshaper.reshape(arabic_text)
    adjust_text = get_display(reshaped_text)
    return adjust_text


if __name__ == '__main__':
    my_post = scrape()
    #print('Done scraping')
    post(my_post)
    #print('Done posting')
