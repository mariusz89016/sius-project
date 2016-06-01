from flask import Flask, Response
import urllib.request
app = Flask(__name__)

@app.route("/random")
def hello():
    image = urllib.request.urlopen("http://source.unsplash.com/random").read()
    return Response(image, mimetype='image/png')

if __name__ == "__main__":
    app.run()
