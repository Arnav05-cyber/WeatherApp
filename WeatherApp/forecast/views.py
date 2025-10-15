from django.shortcuts import render

# Create your views here.

import requests
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import mean_squared_error
from datetime import datetime, timedelta 
import pytz
import os

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

def read_historical_data(filename):
    df = pd.read_csv(filename)
    df = df.dropna()
    df = df.drop_duplicates()
    return df

def prepare_data(data):
    le = LabelEncoder()
    data['WindGustDir'] = le.fit_transform(data['WindGustDir'])
    data['RainTomorrow'] = le.fit_transform(data['RainTomorrow'])


    X = data[['MinTemp', 'MaxTemp', 'WindGustDir', 'WindGustSpeed', 'Humidity', 'Pressure', 'Temp']]
    y = data['RainTomorrow']

    return X,y, le

def train_rain_model(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("Mean squared error for rain model")

    print(mean_squared_error(y_test, y_pred))

    return model

def prepare_regression_data(data, feature):
    X, y = [], []

    for i in range(len(data)-1):
        X.append(data[feature].iloc[i])
        y.append(data[feature].iloc[i+1])

    X = np.array(X).reshape(-1,1)
    y = np.array(y)

    return X,y

def train_regression_model(X,y):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X,y)
    return model

def predict_future(model, current_value):
    predictions = [current_value]

    for i in range(5):
        next_value = model.predict(np.array([[predictions[-1]]]))
        
        predictions.append(next_value[0])

    return predictions[1:]


from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

def weather_view(request):
    logger.info(f"Request method: {request.method}")
    if request.method == 'POST':
        city = request.POST.get('city')
        logger.info(f"City received: {city}")

        current_weather = get_current_weather(city)

        # Try different paths for the CSV file
        csv_paths = [
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'weather.csv'),
            os.path.join('C:\\Weather_App_Deployment\\weather.csv'),
            'weather.csv'
        ]
        
        csv_path = None
        for path in csv_paths:
            if os.path.exists(path):
                csv_path = path
                break
        
        if not csv_path:
            # Create dummy data if CSV not found
            import pandas as pd
            import numpy as np
            dummy_data = {
                'MinTemp': np.random.uniform(15, 25, 100),
                'MaxTemp': np.random.uniform(25, 35, 100),
                'WindGustDir': ['N', 'S', 'E', 'W'] * 25,
                'WindGustSpeed': np.random.uniform(10, 30, 100),
                'Humidity': np.random.uniform(40, 80, 100),
                'Pressure': np.random.uniform(1000, 1020, 100),
                'Temp': np.random.uniform(20, 30, 100),
                'RainTomorrow': ['Yes', 'No'] * 50
            }
            historical_data = pd.DataFrame(dummy_data)
        else:

            historical_data = read_historical_data(csv_path)

        X,y,le = prepare_data(historical_data)

        rain_model = train_rain_model(X,y)

        wind_deg = current_weather['wind_gust_dir'] % 360
        compass_points = [
          ("N", 0, 11.25), ("NNE", 11.25, 33.75), ("NE", 33.75, 56.25),
          ("ENE", 56.25, 78.75), ("E", 78.75, 101.25), ("ESE", 101.25, 123.75),
          ("SE", 123.75, 146.25), ("SSE", 146.25, 168.75), ("S", 168.75, 191.25),
          ("SSW", 191.25, 213.75), ("SW", 213.75, 236.25), ("WSW", 236.25, 258.75),
          ("W", 258.75, 281.25), ("WNW", 281.25, 303.75), ("NW", 303.75, 326.25),
          ("NNW", 326.25, 348.75)
        ]

        compass_direction = next(point for point, start, end in compass_points if start <= wind_deg< end)

        compass_direction_encoded = le.transform([compass_direction])[0] if compass_direction in le.classes_ else -1

        current_data = {
          'MinTemp': current_weather['temp_min'],
          'MaxTemp': current_weather['temp_max'],
          'WindGustDir': compass_direction_encoded,
          'WindGustSpeed': current_weather['wind_gust_speed'],
          'Humidity': current_weather['humidity'],
          'Pressure': current_weather['pressure'],
          'Temp': current_weather['current_temp']
      }

        current_df = pd.DataFrame([current_data])

        rain_prediction = rain_model.predict_proba(current_df)[0][1]  # Get probability of rain (class 1)

        X_temp, y_temp = prepare_regression_data(historical_data, 'Temp')

        X_hum, y_hum = prepare_regression_data(historical_data, 'Humidity')

        temp_model = train_regression_model(X_temp, y_temp)
        hum_model = train_regression_model(X_hum, y_hum)

        future_temp = predict_future(temp_model, current_weather['temp_min'])
        future_humidity = predict_future(hum_model, current_weather['humidity'])

        timezone = pytz.timezone('Asia/Kolkata')
        now = datetime.now(timezone)
        next_hour = now + timedelta(hours=1)
        next_hour = next_hour.replace(minute=0, second=0, microsecond=0) 

        future_times = [(next_hour + timedelta(hours=i)).strftime("%H:00") for i in range(5)]

        time1, time2, time3, time4, time5 = future_times
        temp1, temp2, temp3, temp4, temp5 = future_temp
        hum1, hum2, hum3, hum4, hum5 = future_humidity

        # Calculate rain probability from the model prediction
        rain_probability = int(rain_prediction * 100)

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
            'time1': time1,
            'time2': time2,
            'time3': time3,
            'time4': time4,
            'time5': time5,
            'temp1': f"{round(temp1,1)}°C",
            'temp2': f"{round(temp2,1)}°C",
            'temp3': f"{round(temp3,1)}°C",
            'temp4': f"{round(temp4,1)}°C",
            'temp5': f"{round(temp5,1)}°C",
            'hum1': f"{round(hum1,1)}%",
            'hum2': f"{round(hum2,1)}%",
            'hum3': f"{round(hum3,1)}%",
            'hum4': f"{round(hum4,1)}%",
            'hum5': f"{round(hum5,1)}%",
            # Clean numeric values for chart
            'temp1_num': round(temp1,1),
            'temp2_num': round(temp2,1),
            'temp3_num': round(temp3,1),
            'temp4_num': round(temp4,1),
            'temp5_num': round(temp5,1),
        }

        logger.info(f"Context keys: {list(context.keys())}")
        return render(request, 'weather.html', context)

    return render(request, 'weather.html')