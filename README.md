# Weather Forecast App

A modern, interactive weather application built with Django that provides real-time weather data and temperature forecasting with machine learning predictions.

## Features

- **Real-time Weather Data**: Get current weather conditions for any city worldwide
- **5-Hour Temperature Forecast**: View upcoming temperature predictions with interactive chart
- **Machine Learning Predictions**: Uses Random Forest algorithms for rain probability and temperature forecasting
- **Interactive Chart**: Hover over data points to see exact temperature values
- **Responsive Design**: Beautiful, modern UI that works on all devices
- **Weather Details**: Comprehensive information including humidity, pressure, wind speed, and visibility

## Screenshots

The app features a sleek, modern interface with:
- Current temperature and weather conditions
- 5-hour forecast with temperature and humidity data
- Interactive line chart showing temperature trends
- Rain probability predictions

## Technology Stack

- **Backend**: Django 5.2.7
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js
- **Machine Learning**: scikit-learn (Random Forest)
- **Data Processing**: pandas, numpy
- **Weather API**: OpenWeatherMap API
- **Icons**: Bootstrap Icons

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Weather_App_Deployment
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv myenv
   
   # On Windows
   myenv\Scripts\activate
   
   # On macOS/Linux
   source myenv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django requests pandas numpy scikit-learn pytz
   ```

4. **Set up the project**
   ```bash
   cd WeatherApp
   python manage.py migrate
   ```

5. **Add your weather data**
   - Place your historical weather CSV file at: `C:\Weather_App_Deployment\weather.csv`
   - The CSV should contain columns: MinTemp, MaxTemp, WindGustDir, WindGustSpeed, Humidity, Pressure, Temp, RainTomorrow

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and go to: `http://127.0.0.1:8000/`

## API Configuration

The app uses OpenWeatherMap API for weather data. The API key is currently hardcoded in `views.py`:

```python
API_KEY = '345a7fa85e147e25d2b53bb5b6a9e304'
```

For production, consider moving this to environment variables:

```python
import os
API_KEY = os.getenv('OPENWEATHER_API_KEY', 'your-default-key')
```

## Project Structure

```
Weather_App_Deployment/
├── myenv/                          # Virtual environment
├── WeatherApp/                     # Django project
│   ├── WeatherApp/                 # Project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── forecast/                   # Main app
│   │   ├── static/                 # Static files
│   │   │   ├── css/
│   │   │   ├── js/
│   │   │   └── img/
│   │   ├── templates/              # HTML templates
│   │   │   └── weather.html
│   │   ├── views.py                # Main logic
│   │   ├── models.py
│   │   └── urls.py
│   ├── manage.py
│   └── db.sqlite3
├── weather.csv                     # Historical weather data
└── README.md
```

## How It Works

### Weather Data Flow

1. **User Input**: User enters a city name
2. **API Call**: App fetches current weather from OpenWeatherMap
3. **Data Processing**: Historical data is loaded and processed
4. **ML Predictions**: Random Forest models predict future temperatures and rain probability
5. **Visualization**: Interactive chart displays temperature trends
6. **Display**: All data is presented in a modern, responsive interface

### Machine Learning Models

The app uses two Random Forest models:

1. **Rain Prediction Model**: Predicts probability of rain based on weather conditions
2. **Temperature Forecasting**: Predicts future temperatures using historical patterns

### Chart Features

- **Interactive Line Chart**: Built with Chart.js
- **Hover Tooltips**: Show exact temperature and time on hover
- **Smooth Animations**: Elegant loading animations
- **Responsive Design**: Adapts to different screen sizes

## Usage

1. **Search for Weather**: Enter any city name in the search box
2. **View Current Conditions**: See temperature, humidity, pressure, and other details
3. **Check Forecast**: View 5-hour temperature and humidity predictions
4. **Interact with Chart**: Hover over data points to see exact values
5. **Rain Probability**: Check the ML-predicted chance of rain

## Customization

### Styling
- Modify `forecast/static/css/styles.css` for visual changes
- Chart colors and styling can be adjusted in the JavaScript section of `weather.html`

### API Settings
- Change the API endpoint or add new weather services in `views.py`
- Modify the data processing logic for different weather parameters

### Machine Learning
- Update the CSV file path in `views.py` for different datasets
- Adjust model parameters for better predictions
- Add new features to the prediction models

## Troubleshooting

### Common Issues

1. **Django not found**: Make sure virtual environment is activated
2. **API errors**: Check internet connection and API key validity
3. **CSV file not found**: Ensure weather.csv is in the correct location
4. **Chart not displaying**: Check browser console for JavaScript errors

### Debug Mode

The app runs in debug mode by default. For production:

```python
# In settings.py
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues and questions:
- Check the troubleshooting section
- Review Django and Chart.js documentation
- Open an issue in the repository

## Future Enhancements

- [ ] Extended forecast (7-day, 14-day)
- [ ] Weather maps integration
- [ ] User location detection
- [ ] Weather alerts and notifications
- [ ] Historical weather data visualization
- [ ] Multiple city comparison
- [ ] Weather widgets for embedding

---

**Built with ❤️ using Django and modern web technologies**