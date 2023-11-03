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

        metrics["last_update"] = prometheus_client.Gauge(
            "hcmetrics_last_update", "Last update of metrics"
        )


        metrics["values"] = prometheus_client.Gauge(
            "rego637_raw", "Value of index idx", ["idx"]
        )
        metrics["0001"] = prometheus_client.Gauge(
            "radiator_return", "Temperature of return water feed in degree C"
        )
        metrics["0003"] = prometheus_client.Gauge(
            "heat_carrier_return", "Temperature of heat carrier return in degree C"
        )
        metrics["0004"] = prometheus_client.Gauge(
            "heat_carrier_forward", "Temperature of heat carrier forward in degree C"
        )
        metrics["0005"] = prometheus_client.Gauge(
            "evaporator", "Temperature of evaporator/brine in in degree C"
        )
        metrics["0006"] = prometheus_client.Gauge(
            "condenser", "Temperature of condenser/brine out in degree C"
        )
        metrics["0007"] = prometheus_client.Gauge(
            "outdoor", "Temperature of outdoor sensor in degree C"
        )
        metrics["0009"] = prometheus_client.Gauge(
            "warmwater", "Temperature of top of warmwater in degree C"
        )
        metrics["000B"] = prometheus_client.Gauge(
            "hotgas", "Temperature of hot gas/compressor in degree C"
        )
        metrics["0107"] = prometheus_client.Gauge(
            "heating_setpoint", "Desired temperature of room in degree C"
        )
        metrics["0111"] = prometheus_client.Gauge(
            "warmwater_setpoint", "Desired temperature of warmwater in degree C"
        )
        metrics["0203"] = prometheus_client.Gauge(
            "room_setpoint", "Desired temperature of room in degree C (writable)"
        )
        metrics["2205"] = prometheus_client.Gauge(
            "heat_set1", "Heat set 1 (curveL) (writable)"
        )
        metrics["3104"] = prometheus_client.Gauge(
            "add_heatstatus", "Percent of additional heating applied"
        )
        metrics["0207"] = prometheus_client.Gauge(
            "heat_set3", "Heat set 3 (parallell) (writable)"
        )
        metrics["0208"] = prometheus_client.Gauge(
            "warmwater_stoppoint", "Warm water stop temperatur in degree C (writable)"
        )
        metrics["020B"] = prometheus_client.Gauge(
            "warmwater_difference", "Warm water allowed difference in degree C (writable)"
        )
        metrics["7209"] = prometheus_client.Gauge(
            "extra_warmwater", "Extra warm water in minutes (writable)"
        )
        metrics["1215"] = prometheus_client.Gauge(
            "heater_switch", "Electric heater enabled/disabled, used upon next heater start (writable)"
        )
        metrics["020A"] = prometheus_client.Gauge(
            "summer_mode", "Temp where summer mode (hot water only) is activated in degree C (writable)"
        )
        metrics["0210"] = prometheus_client.Gauge(
            "holiday_mode", "Holiday mode in hours (writable)"
        )
        metrics["1A01"] = prometheus_client.Gauge(
            "compressor", "Compressor status (0=off, 1=on)"
        )
        metrics["1A02"] = prometheus_client.Gauge(
            "addheatstep1", "Additional heat (normally 3kW) status (0=off, 1=on)"
        )
        metrics["1A03"] = prometheus_client.Gauge(
            "addheatstep2", "Additional heat (normally 6kW) (0=off, 1=on)"
        )
        metrics["1A05"] = prometheus_client.Gauge(
            "pumpheatcircuit", "Heat circuit status (0=off, 1=on)"
        )
        metrics["1A06"] = prometheus_client.Gauge(
            "pumpradiator", "Radiator pump status (0=off, 1=on)"
        )
        metrics["1A07"] = prometheus_client.Gauge(
            "switchvalve", "Switch valve position (0=radiator, 1=hot water)"
        )
        metrics["1A20"] = prometheus_client.Gauge(
            "pumpalarm", "Alarm (active if >0)"
        )
        metrics["BA91"] = prometheus_client.Gauge(
            "alarmcode", "Last alarm triggered"
        )
        metrics["6C55"] = prometheus_client.Gauge(
            "compressorheating", "Compressor runtime for heating"
        )
        metrics["6C56"] = prometheus_client.Gauge(
            "compressorhotwater", "Compressor runtime for hot water"
        )
        metrics["6C58"] = prometheus_client.Gauge(
            "auxheating", "Electric additon runtime for heating"
        )
        metrics["6C59"] = prometheus_client.Gauge(
            "auxhotwater", "Electric addition runtime for hot water"
        )


    def refresh_all_meters(self):
        url = f"{BASEURL}/api/alldata"
        js = {}
        rawvalue = ('3104', '1215', '1233', '1A01', '1A02','1A03', '1A04', '1A05','1A06','1A07','1A20','BA91', '6C55', '6C56', '6C58','6C59')
        with urllib.request.urlopen(url) as data:
            if data.status == 200:
                js = json.loads(data.read())
        for p in js:
            self.metrics["values"].labels(idx=p).set(js[p])

            if p in self.metrics:
                if p in rawvalue:
                    self.metrics[p].set(js[p])
                else:
                    self.metrics[p].set(js[p]/10)

        self.metrics["last_update"].set(time.time())

def serve():
    meter = Meter()
    meter.refresh_all_meters()

    prometheus_client.start_http_server(8010)

    while True:
        time.sleep(20)
        try:
            meter.refresh_all_meters()
        except OSError as e:
            print(f"Ignoring exception {e}")


if __name__ == "__main__":
    serve()
