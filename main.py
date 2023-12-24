import BlynkLib
import network
import time
import machine
import time
from blynktimer import Timer
def handle_wifi():

    wlan.active(True)
    wlan.connect(ssid, password)

    # Wait for connect or fail
    max_wait = 20
    while max_wait > 0:
        if wlan.status() ==  network.STAT_GOT_IP:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)
        
            # Handle connection error
    if wlan.status() != network.STAT_GOT_IP:
        raise Exception ("Not able to connect to WiFi. Resetting the system")
    else:
        print('connected')
        led.on()
        status = wlan.ifconfig()
        print( 'ip = ' + status[0] )


try:
    # Initialize Blynk
    adc = machine.ADC(4)
    ssid = "YOUR_SSID"
    password = 'YOIR_PASSWROD'
    led = machine.Pin("LED", machine.Pin.OUT)
    BLYNK_AUTH= "YOUR_BLYNK_AUTH"
    BLYNK_TEMPLATE_ID = "YOUR_BLYNK_TEMPLATE"
    wlan = network.WLAN(network.STA_IF)
    relay_in    = machine.Pin(28, mode=machine.Pin.OUT)
    handle_wifi()
    blynk = BlynkLib.Blynk(BLYNK_AUTH,server='blynk.cloud')
    blynk_timer  = Timer()

    @blynk.VIRTUAL_WRITE(0)
    def my_read_handler(data_fetched):
        relay_in.value(int(data_fetched[0]))
        #relay_in.toggle()

        # this widget will show some time in seconds..
        print(data_fetched[0])
        
    @blynk.ON("disconnected")
    def blynk_disconnected():
        raise Exception ('Blynk disconnected')
        

    @blynk.ON("connected")       
    def blynk_connected():
        # You can also use blynk.sync_virtual(pin)
        # to sync a specific virtual pin
        print("Updating V1,V2,V3 values from the server...")
        blynk.sync_virtual(1,2,3)
    @blynk_timer.register(interval=1)
    def temperature():
        ADC_voltage = adc.read_u16() * (3.3 / (65536))
        temperature_celcius = 27 - (ADC_voltage - 0.706)/0.001721
        print("Temperature: {}°C".format(temperature_celcius))
        blynk.virtual_write(2, str(temperature_celcius))

    blynk.run()
    blynk.sync_virtual(0,1,2)
    while True:
        wlan_status = wlan.status()
        if wlan_status != network.STAT_GOT_IP:
            print("Reseting wifi")
            raise Exception ("Resetting the system. Disconnection detected")
    
        blynk.run()
        blynk_timer.run()
except Exception as e:
    print(e)
    led.off()
    relay_in.off()
    machine.reset()








