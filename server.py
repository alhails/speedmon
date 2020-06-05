from flask import Flask, request, send_from_directory, render_template
import json

app = Flask(__name__, static_url_path="")
 
@app.route("/", defaults = {'path':''})
@app.route("/<path:path>")
def interface(path):
    if path == '':
        return render_template("speedmon.html")
    return send_from_directory('static', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)
 
@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route("/results", methods=["GET"])
def wakeup():
    status = 200
    success = True

    file1 = open("data/speedmon.log", "r")
    lines = file1.readlines()

    results = []
    for line in lines:
        items = line.split(",")
        result = Result(items[1].rstrip(), items[0])
        results.append(result)
            
    return json.dumps([o.__dict__ for o in results]), status, {'ContentType': 'application/json'}

class Result():
    def __init__(self, rate, ts):
        self.rate = rate
        self.ts = ts

if __name__ == "__main__":
    app.run(host='0.0.0.0')

