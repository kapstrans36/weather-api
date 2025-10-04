from django.shortcuts import render

# Create your views here.
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.shortcuts import render

@api_view(['GET'])
def get_weather(request):
    city = request.GET.get('city')
    if not city:
        return Response({"error": "City parameter is required"}, status=400)

    api_key = settings.WEATHER_API_KEY
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city }&appid={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses
        weather_data = response.json()

        context= {
            "city": weather_data['name'],
            "temperature_celsius": weather_data['main']['temp'],
            "description": weather_data['weather'][0]['description']
        }
        return render(request, 'map.html', context)
        return Response(data_to_send)

    except requests.exceptions.RequestException:
        return Response({"error": "Failed to fetch weather data"}, status=500)
    except KeyError:
        return Response({"error": "Invalid city or data structure"}, status=404)
