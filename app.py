from flask import Flask,jsonify,request
import requests
import redis
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import ast

load_dotenv()

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per minute"]
)

redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    decode_responses=True

)

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"


@app.route('/weather/<city>',methods=['GET'])
# @limiter.limit("10 per minute")
def get_weather(city):
    cached_data = redis_client.get(city)

    if cached_data:
        return jsonify({"source": "cache", "data": ast.literal_eval(cached_data)})

    

    try:
        response = requests.get(f'{BASE_URL}/{city}', params={"key": API_KEY})
        response.raise_for_status()
        fetched_data = response.json()

        # cache the result with 12 hour expiration 
        redis_client.setex(city,12*60*60,str(fetched_data))
        return jsonify({"source":"api","data": fetched_data})
    except requests.exceptions.RequestException as e:
        return jsonify({"error":"Failed to fetch the weather data","details": str(e)}),500
    
@app.errorhandler(429)
def rate_limit_exceed(e):
    return jsonify({"error": "Rate limit exceeded","message":str(e.description)}),429


if __name__ == '__main__':
    app.run(debug=True)