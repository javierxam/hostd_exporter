import requests
from prometheus_client import Gauge
import http.server
import prometheus_client

#port for serving the metrics
portExporter=8000
apiPort="9980"
apiIP="192.168.0.10"

#web request for getting data from hostd and serialize in to a json object
url = "http://"+apiIP+":"+apiPort+"/api/metrics"
payload={}
headers = {}
data = requests.request("GET", url, headers=headers, data=payload, auth=("xavi", "Xamxamxam666%"))
js=data.json()


#get data from keys storage
storageMetrics=js["storage"]
totalSectors=storageMetrics['totalSectors']
storageTotalBytes=totalSectors*4*1024*1024
storagePhisical=storageMetrics['physicalSectors']
storagePhisicalBytes=storagePhisical*4*1024*1024

storage_total = Gauge('hostd_storage_total_size_bytes','total storage asigned to hostd')
storage_total.set(storageTotalBytes)
phisical_bytes = Gauge('hostd_storage_phisical_bytes','phisical bytes used by hostd')
phisical_bytes.set(storagePhisicalBytes)

#get data from keys contracts
contractsMetrics=js["contracts"]
contractsActiveMetrics=contractsMetrics['active']
contractsSuccesfulMetrics=contractsMetrics['successful']

contracts_active = Gauge('hostd_contracts_active','contracts active in hostd')
contracts_active.set(contractsActiveMetrics)
contracts_succesful = Gauge('hostd_contracts_succesful','contracts succesful in hostd')
contracts_succesful.set(contractsSuccesfulMetrics)

contractsLockedCollateralMetrics=round((float(contractsMetrics['lockedCollateral'])/1000000000000000000000000), 0)
contractsRiskedCollateralMetrics=round((float(contractsMetrics['riskedCollateral'])/1000000000000000000000000), 0)

locked_collateral = (Gauge('hostd_locked_collateral','locked collateral in hostd'))
locked_collateral.set(contractsLockedCollateralMetrics)
risked_collateral = Gauge('hostd_risked_collateral','risked collateral in hostd')
risked_collateral.set(contractsRiskedCollateralMetrics)



class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/metrics':
            # return a json with metrics
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(prometheus_client.generate_latest())
        else:
            # return message error
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')


# make an instance of ThreadingHTTPServer on port declared in portExporter
server = http.server.ThreadingHTTPServer(('', portExporter), MyHandler)

# start the server
server.serve_forever()
