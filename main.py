# import flask to setup web server
from flask import Flask, request
# import redis for storing tries
import redis
import os

app = Flask(__name__)

client = redis.Redis(
    host = os.environ.get('REDIS_HOST'),
    port = os.environ.get('REDIS_PORT'),
    password = os.environ.get('REDIS_PASSWORD')
)

@app.route('/', methods=['GET'])
def index():
    return '''
    Hello World
    <br>
    <br>
    Insertion by
    <br>
    /insert?query=history
    <br>
    /insert?query=historical
    <br>
    /insert?query=histogram
    <br>
    <br>
    Searching by
    <br>
    <a href='/search?query=his'>/search?query=his</a>
    <br>
    <br>
    <a href='https://github.com/ayush02av/redis-search' target='_blank'>Source code</a>
    '''

@app.route('/insert', methods=['GET'])
def insert():
    if 'query' not in request.args.keys():
        return 'No query given. Example: /insert?query=majnu ka tila'
        
    query = request.args['query'].lower()
    
    if len(query) > 15:
        return 'query should be less than 15 characters'

    for i in range(len(query)):
        key = query[0:i+1]

        if i == len(query) - 1:
            if client.exists(key):
                client.hset(key, 'count', int(client.hget(key, 'count').decode('utf8')) + 1)
            else:
                client.hset(key, 'count', 1)
                client.hset(key, 'end', 1)
        else:
            next_key = query[i + 1]

            if client.exists(key):
                client.hset(key, 'count', int(client.hget(key, 'count').decode('utf8')) + 1)
                
                if client.hexists(key, next_key):
                    client.hset(key, next_key, int(client.hget(key, next_key).decode('utf8')) + 1)
                else:
                    client.hset(key, next_key, 1)
            else:
                client.hset(key, 'count', 1)
                client.hset(key, 'end', 0)
                client.hset(key, next_key, 1)
    
    return 'inserted'

def helper(key, results):
    data = client.hgetall(key)

    if data[b'end'] == b'1':
        results.append(key)
        return results
    
    del data[b'count']
    del data[b'end']
    
    for data_key in data.keys():
        results = helper(key + data_key.decode('utf8'), results)

    # return results
    return results

@app.route('/search', methods=['GET'])
def search():
    if 'query' not in request.args.keys():
        return 'No query given. Example: /insert?query=majnu ka tila'
        
    query = request.args['query'].lower()
    
    if len(query) > 15:
        return 'query should be less than 15 characters'
    
    i = len(query) - 1
    while i >= 0:
        key = query[0:i+1]
        if client.exists(key):
            break
        i -= 1

    return ','.join(helper(query[0:i+1], []))

if __name__ == "__main__":
    app.run(port=80, debug=True)