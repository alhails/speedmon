from flask import Flask, request, send_from_directory, render_template
import json

app = Flask(__name__, static_url_path="")
 
@app.route("/", defaults = {'path':''})
@app.route("/<path:path>")
def interface(path):
    return render_template("speedmon.html")

@app.route("/results", methods=["GET"])
def results():
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

