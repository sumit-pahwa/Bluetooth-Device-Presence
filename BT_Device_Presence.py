import gspread
from oauth2client.service_account import ServiceAccountCredentials
import subprocess
import time
import csv

# setting up devices: DeviceName, DeivceMac, DeviceOwner
deviceList =[]
with open('/home/pi/Documents/Python_Projects/BT_iPhone/devices.csv', 'r', encoding="utf-8") as deviceFile:
    readCSV = csv.reader(deviceFile, delimiter=',')
    for row in readCSV:
        curr_device = [row[0], row[1], row[2]]
        deviceList.append(curr_device)


#setting up google spreadsheets 
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/Documents/Python_Projects/BT_iPhone/client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open("PawaHousePresenceLog").sheet1
 




#look for device
def findDevice(deviceName, deviceMac):
    device_Status = (subprocess.check_output(["hcitool","name", deviceMac]).decode("utf-8")).strip('\n')
    print(deviceName)
    print(device_Status)
    if device_Status == deviceName:
        return(1)
    else:
        return(0)

for n in deviceList:
    if findDevice(n[0],n[1])==1:
        sheet.insert_row(["found",n[0], n[1], time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S")],2)
    else:
        sheet.insert_row(["Not found", n[0], n[1], time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S")],2)


        
  
