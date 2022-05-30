import json
from urllib import request
from flask import Flask, render_template, jsonify
import time
import datetime
import redis
import requests

app = Flask(__name__)

redis_cache = redis.Redis(host='localhost', port=6379,db=0, password="")

# 1. Use Redis to enhance secondary respond times from these end points.
@app.route('/fetch1')
def url1():
    url = "https://datausa.io/api/data?University=142832&measures=Total%20Noninstructional%20Employees&drilldowns=IPEDS%20Occupation&parents=true"
    if redis_cache.get(url):
        start = datetime.datetime.now()
        print('its cached')
        value = redis_cache.get(url)
        end = datetime.datetime.now()
        total_time = end-start
        execution_time = total_time.total_seconds() * 1000
        value_snippet = json.loads(value)
        time_taken = str(round(execution_time,2)) + ' ms.'
        return jsonify('request time: {} Response: {}'.format(time_taken,value_snippet))
    else:
        print('its not cached')
        start = datetime.datetime.now()
        response = requests.get(url).json()
        end = datetime.datetime.now()
        total_time = end-start
        execution_time = total_time.total_seconds() * 1000
        response_snippet = response['data'][0]
        redis_cache.set(url, json.dumps(response_snippet))
        time_taken = str(round(execution_time,2)) + ' ms.'
        return jsonify('request time: {} Response: {}'.format(time_taken, response_snippet))
    

# 1. Use Redis to enhance secondary respond times from these end points.
@app.route('/fetch2')
def url2():
    url = "https://datausa.io/api/data?measures=Average%20Wage,Average%20Wage%20Appx%20MOE&drilldowns=Detailed%20Occupation"
    if redis_cache.get(url):
        start = datetime.datetime.now()
        print('its cached')
        value = redis_cache.get(url)
        end = datetime.datetime.now()
        total_time = end-start
        execution_time = total_time.total_seconds() * 1000
        value_snippet = json.loads(value)
        time_taken = str(round(execution_time,2)) + ' ms.'
        return jsonify('request time: {} Response: {}'.format(time_taken,value_snippet))
    else:
        print('its not cached')
        start = datetime.datetime.now()
        response = requests.get(url).json()
        end = datetime.datetime.now()
        total_time = end-start
        execution_time = total_time.total_seconds() * 1000
        response_snippet = response['data'][0]
        redis_cache.set(url, json.dumps(response_snippet))
        time_taken = str(round(execution_time,2)) + ' ms.'
        return jsonify('request time: {} Response: {}'.format(time_taken, response_snippet))

# 2. Make use Redis to drill down in to the data and find some interesting point that can be fetched and displayed without the need to re-query the API all the time.
@app.route('/find/fetch1')
def find_university_id():
    response = redis_cache.get("https://datausa.io/api/data?University=142832&measures=Total%20Noninstructional%20Employees&drilldowns=IPEDS%20Occupation&parents=true")
    response = json.loads(response)
    uni_id = response['ID University']
    return jsonify('University id found: {}'.format(uni_id))


# 3. Divide the data in to logical divisions using either sets, lists,hashed or one of the other types native to Redis.
# 4. Specify a retention time for all values (Time to live)
@app.route('/divide')
def divide_data():
    data = requests.get('https://datausa.io/api/data?University=142832&measures=Total%20Noninstructional%20Employees&drilldowns=IPEDS%20Occupation&parents=true/')
    data_json = data.json()
    for number, api_object in enumerate(data_json['data']):
        for key, value in api_object.items():
            redis_cache.hset(number, key, value)
        redis_cache.expire(number, 3600)
    value = redis_cache.hget("9","University")
    value = value.decode('utf-8')
    return jsonify(value)



if __name__ == "__main__":
    app.run(debug=True, port=5005)

    
