from machine import Pin
from time import sleep
import dht
import utime
import microdot
from microdot import Microdot
from microdot import send_file

humedad = 0
sensor = dht.DHT11(Pin(2))
app = Microdot()

def handle_client(conn, addr):
    conn.close()

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('Red Profesores', 'Profes_IMPA_2022')
        
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    
    return wlan.ifconfig()[0]


addr = (do_connect(), 80)

print("listening on {}".format(addr))



@app.route('/')
def index(request):
     #print("\nEnviando index.html")
     return send_file("index.html")

@app.route("/assets/<dir>/<file>")
def assets(request, dir, file):
    #print("enviando: ", file)
    return send_file("/assets/" + dir + "/" + file)

@app.route("/data/update")
def info(request):
    
    sensor.measure()
    humedad = sensor.humidity()
    #print('Humidity: %3.1f %%' %humedad)
   
    dic = { "data" : humedad}
    #print("enviando..")
    return dic

app.run(port=80)

    
    
    
    
    
    
