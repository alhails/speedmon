from flask import Flask, request, send_from_directory, render_template
import json
import pexpect
import configparser

app = Flask(__name__, static_url_path="")
 
@app.route("/", defaults = {'path':''})
@app.route("/<path:path>")
def interface(path):
    return render_template("speedmon.html")

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route("/results", methods=["GET"])
def results():
    status = 200

    file1 = open("data/speedmon.log", "r")
    lines = file1.readlines()

    results = []
    for line in lines:
        items = line.split(",")
        result = Result(items[0], items[1].rstrip(), items[2].rstrip())
        results.append(result)
            
    return json.dumps([o.__dict__ for o in results]), status, {'ContentType': 'application/json'}

class Result():
    def __init__(self, ts, dl, ul):
        self.ts = ts
        self.dl = dl
        self.ul = ul

@app.route("/uptime", methods=["GET"])
def uptime():
    status = 200
    uptime = Uptime("00:00")

    config = configparser.ConfigParser()
    config.read('server.cfg')
    server = config.get('uptime', 'server')
    uid = config.get('uptime', 'uid')
    pwd = config.get('uptime', 'pwd')

    child = pexpect.spawn("telnet {0}".format(server))
    child.expect("login:")
    child.send("{0}\r".format(uid))
    child.expect("Password:")
    child.send("{0}\r".format(pwd))
    child.expect("#")
    child.send("uptime\r")

    # 13:18:40 up  7:42,  1 users,  load average: 0.29, 0.36, 0.41
    child.expect("up *(\d+:\d+)?(?:(\d+) min)?,")
    if child.match:
        hoursMin = child.match.group(1)
        hours = 0
        mins = 0
        if hoursMin:
            uptimeSplit = hoursMin.decode().split(":")
            hours = int(uptimeSplit[0])
            mins = int(uptimeSplit[1])

        minsMatch = child.match.group(2)
        if minsMatch:
            mins = int(minsMatch.decode())

        uptime = Uptime("{0:02d}:{1:02d}".format(hours, mins))

    child.close()

    return json.dumps(uptime.__dict__), status, {'ContentType': 'application/json'}

class Uptime():
    def __init__(self, uptime):
        self.uptime = uptime

if __name__ == "__main__":
    app.run(host='0.0.0.0')

