from flask import Flask,request,render_template
import requests
import os
from dotenv import load_dotenv
load_dotenv()
app=Flask(__name__)
app.secret_key = "123"

API_KEY = os.getenv("WEATHER_API_KEY")
@app.route("/")
def index():
    return render_template("weather.html")

@app.route("/city",methods=['GET','POST'])
def city():
    try:
        city=request.form['city']
        print(city)
        api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"
        respons = requests.get(api)
        data = respons.json()
        print(data)

        if data['cod'] != 200:
            error_message = "City not found or invalid city name. Please try again."
            return render_template("weather.html", error_message=error_message)

        country=data['sys']['country']
        temp=data['main']['temp']
        temp_min=data['main']['temp_min']
        temp_max=data['main']['temp_max']
        feel_like=data['main']['feels_like']
        icon=data['weather'][0]['icon']
        cloud=data['weather'][0]['main']
        return render_template("weather.html",cloud=cloud,city=city,country=country,temp=temp,max=temp_max,min=temp_min,feel=feel_like,icon=icon)

    except Exception as e:
        print(str(e))

if __name__=="__main__":
    app.run(host="0.0.0.0",port=3000)



