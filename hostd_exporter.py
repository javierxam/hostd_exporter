import requests
from prometheus_client import Gauge
import http.server
import prometheus_client


url = "http://192.168.0.10:9980/api/metrics"
payload={}
headers = {}
datos = requests.request("GET", url, headers=headers, data=payload, auth=("xavi", "Xamxamxam666%"))
js=datos.json()

stor=js["storage"]
storNew=stor['totalSectors']
storNew=storNew*4*1024*1024
print(storNew)

storage_total = Gauge('storage_total_size_bytes','total storage asigned to hostd')
storage_total.set(storNew)
class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/metrics':
            # Devolvemos el json con las metricas
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(prometheus_client.generate_latest())
        else:
            # Devolvemos un mensaje de error
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')



# Creamos una instancia de ThreadingHTTPServer en el puerto 8000
server = http.server.ThreadingHTTPServer(('', 8001), MyHandler)

# Iniciamos el servidor
server.serve_forever()
