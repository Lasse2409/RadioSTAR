import socket
import time
from src.utilities import utilities


class rotor:
    def __init__(self, IP, port):
        self.IP = IP
        self.port = port

        self.az = 0
        self.el = 0

        self.PH = 10
        self.PV = 10

        self.overwrite = False

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.IP, self.port))
        print("Rotor connected")
        self.statusInt()

    def setInt(self, az, el):
        if self.overwrite == False and el < 0:
            return("Cannot set roter to el less than 0")


        H = self.PH*(360 + az)
        V = self.PV*(360 + el)

        HString = str(H)
        VString = str(V)
    
        while len(HString) < 4:
            HString = "0" + HString
    
        while len(VString) < 4:
            VString = "0" + VString
    
        self.client.send(bytes([
            0x57,
            48 + int(HString[0]),
            48 + int(HString[1]),
            48 + int(HString[2]),
            48 + int(HString[3]),
            self.PH,
            48 + int(VString[0]),
            48 + int(VString[1]),
            48 + int(VString[2]),
            48 + int(VString[3]),
            self.PV,
            0x2F,
            0x20
        ]))
        
    def set(self, ez, el):
        self.setInt(ez, el)
        time.sleep(0.5)
        self.statusInt()
        time.sleep(0.5)
        self.statusInt()
        
        oldaz = self.az
        oldel = self.el

        time.sleep(0.5)
        self.statusInt()

        while oldaz != self.az or oldel != self.el:
            oldaz = self.az
            oldel = self.el

            time.sleep(0.5)

            self.statusInt()
            #self.status()


    def stop(self):
        self.client.send(bytes([0x57, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0F, 0x20]))

    def statusInt(self):
        self.client.send(bytes([0x57, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F, 0x20]))
        data = self.client.recv(1024)

        self.az =  int(data[1])*100 + int(data[2])*10 + int(data[3]) + int(data[4])*0.1 - 360
        self.el =  int(data[6])*100 + int(data[7])*10 + int(data[8]) + int(data[9])*0.1 - 360

        self.PH = int(data[5])
        self.PV = int(data[10])

    def status(self):
        self.statusInt()
        print("Az = " + str(self.az + utilities.azElOffset[0]) + ", El = " + str(self.el + utilities.azElOffset[1])) # + ", PH = " + str(self.PH) + ", PV = " + str(self.PV)
        return self.az + utilities.azElOffset[0], self.el + utilities.azElOffset[1]

    def disconnect(self):
        self.client.close()
        print("Rotor disconnected")
