# Overview

speedmon generates download speed metrics speedtest-cli (https://www.speedtest.net/apps/cli)
The results can be returned in csv format and aggregated to provide data for chart

There are two components - 
* speedmon.py
  This provides a simple cli to execute speedtest-cli and parse the results so we can store them in a csv
* server.py
  Flask web app used to expose csv data via web page

# Install

* Create a cron job to execute speedmon.py and append csv results to a file
* Host the Flask web app in web server (e.g. gunicorn)



