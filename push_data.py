import os
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

influx_ip = os.environ['INFLUX_IP']
influx_port = os.environ['INFLUX_PORT']
influx_org = os.environ['INFLUX_ORG']
influx_token = os.environ['INFLUX_TOKEN']
influx_bucket = os.environ['INFLUX_BUCKET']

user="userA"

def make_point(field_name, field_value, tagName, tagValue):
        return Point("weight_data").tag(tagName, tagValue).field(field_name, field_value)

def store_weight_data(field_name, field_value, write_api):
      point = make_point(field_name, field_value, "user", user)
      write_api.write(bucket=influx_bucket, record=point)

def store_data(weight_data):
    print('Pushing data')
    url="http://"+influx_ip+":"+str(influx_port)
    client =  InfluxDBClient(url, token=influx_token, org=influx_org,verify_ssl=False)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    for key, value in weight_data.items():
          store_weight_data(key, value, write_api)