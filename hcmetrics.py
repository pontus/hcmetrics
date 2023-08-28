#!/usr/bin/env python3

import prometheus_client

import time
import urllib.request
import time
import json

BASEURL="http://192.168.25.196"


class Meter():
    data = {}
    metrics =  {}

    def __init__(self):
        metrics = self.metrics

        metrics["value"] = prometheus_client.Gauge(
            "value", "Value of index idx", ["idx"]
        )

    def refresh_all_meters(self):
        url = f"{BASEURL}/api/alldata"
        js = {}
        with urllib.request.urlopen(url) as data:
            if data.status == 200:
                js = json.loads(data.read())
        for p in js:
            self.metrics["value"].labels(idx=p).set(js[p])


def serve():
    meter = Meter()
    prometheus_client.start_http_server(8010)

    while True:
        time.sleep(20)
        meter.refresh_all_meters()


if __name__ == "__main__":
    serve()
