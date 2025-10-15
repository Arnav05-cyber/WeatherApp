from django.shortcuts import render
import requests
from datetime import datetime, timedelta 
import pytz
import random

API_KEY = '345a7fa85e147e25d2b53bb5b6a9e304'
BASE_URL = 'https://api.openweathermap.org/data/2.5/'

def get_current_weather(city):
    url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    return {
        'city': data['name'],
        'current_temp': round(data['main']['temp']),
        'feels_like': round(data['main']['feels_like']),
        'temp_min': round(data['main']['temp_min']),
        'temp_max': round(data['main']['temp_max']),
        'humidity': round(data['main']['humidity']),
        'description': data['weather'][0]['description'],
        'country': data['sys']['country'],
        'wind_gust_dir': data['wind']['deg'],
        'pressure': data['main']['pressure'],
        'wind_gust_speed': data['wind']['speed'],
        'clouds': data['clouds']['all'],
        'visibility': data['visibility'],
    }

def generate_simple_forecast(current_temp, current_humidity):
    """Generate simple forecast without ML dependencies"""
    temps = []
    humidities = []
    
    # Simple temperature variation (±3°C)
    for i in range(5):
        variation = random.uniform(-3, 3)
        new_temp = current_temp + variation
        temps.append(round(new_temp, 1))
    
    # Simple humidity variation (±10%)
    for i in range(5):
        variation = random.uniform(-10, 10)
        new_humidity = max(0, min(100, current_humidity + variation))
        humidities.append(round(new_humidity, 1))
    
    return temps, humidities

def weather_view(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        current_weather = get_current_weather(city)
        
        # Generate simple forecasts
        future_temp, future_humidity = generate_simple_forecast(
            current_weather['current_temp'], 
            current_weather['humidity']
        )
        
        # Simple rain probability based on humidity and clouds
        rain_prediction = (current_weather['humidity'] + current_weather['clouds']) / 200
        rain_probability = int(rain_prediction * 100)

        timezone = pytz.timezone('Asia/Kolkata')
        now = datetime.now(timezone)
        next_hour = now + timedelta(hours=1)
        next_hour = next_hour.replace(minute=0, second=0, microsecond=0) 

        future_times = [(next_hour + timedelta(hours=i)).strftime("%H:00") for i in range(5)]

        time1, time2, time3, time4, time5 = future_times
        temp1, temp2, temp3, temp4, temp5 = future_temp
        hum1, hum2, hum3, hum4, hum5 = future_humidity

        context = {
            'location': city,
            'current_temp': current_weather['current_temp'],
            'MinTemp': current_weather['temp_min'],
            'MaxTemp': current_weather['temp_max'],
            'feels_like': current_weather['feels_like'],
            'humidity': current_weather['humidity'],
            'clouds': current_weather['clouds'],
            'description': current_weather['description'],
            'city': current_weather['city'],
            'country': current_weather['country'],
            'time': datetime.now(),
            'date': datetime.now().strftime("%B %d, %Y"),
            'wind': current_weather['wind_gust_speed'],
            'pressure': current_weather['pressure'],
            'visibility': current_weather['visibility'],
            'rain_probability': rain_probability,
            'time1': time1, 'time2': time2, 'time3': time3, 'time4': time4, 'time5': time5,
            'temp1': f"{temp1}°C", 'temp2': f"{temp2}°C", 'temp3': f"{temp3}°C", 
            'temp4': f"{temp4}°C", 'temp5': f"{temp5}°C",
            'hum1': f"{hum1}%", 'hum2': f"{hum2}%", 'hum3': f"{hum3}%", 
            'hum4': f"{hum4}%", 'hum5': f"{hum5}%",
            'temp1_num': temp1, 'temp2_num': temp2, 'temp3_num': temp3, 
            'temp4_num': temp4, 'temp5_num': temp5,
        }

        return render(request, 'weather.html', context)

    return render(request, 'weather.html')