from flask import Flask, Response, request, abort
import time
import urllib.request
import random

app = Flask(__name__)

DEFAULT_TIMEOUT = 2000 # in milliseconds
DEFAULT_CHANCE = 0.8 # percent

def get_timeout_in_seconds(timeout_millis):
    return timeout_millis / 1000

@app.route("/random")
def random_image():
    timeout = int(request.args.get('timeout', DEFAULT_TIMEOUT))
    random_chance = float(request.args.get('chance', DEFAULT_CHANCE))
    if random.random() < random_chance:
        sleep_time = random.uniform(0, get_timeout_in_seconds(timeout))
        print("Timeout - %s" % sleep_time)
        time.sleep(sleep_time)
        image = urllib.request.urlopen("http://source.unsplash.com/random").read()
        return Response(image, mimetype='image/png')
    else:
        return abort(500)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
