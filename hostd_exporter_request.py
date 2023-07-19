import requests
from prometheus_client import start_http_server,  Summary
import http.server

url = "http://192.168.0.10:9980/api/metrics"
payload={}
headers = {}
datos = requests.request("GET", url, headers=headers, data=payload, auth=("xavi", "Xamxamxam666%"))
js=datos.json()


print (js)

storage_total = Summary('storage_total_size_bytes', 'storage size in bytes')




client.start_http_server(6666)

