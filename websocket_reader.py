import websocket
import json
import threading

class WebsocketReader():
    def __init__(self):
       self.ws = websocket.WebSocketApp("wss://yorkfs.emperorservers.com/api/race-control",
                            on_message=self.on_message,
                            on_error=self.on_error,
                            on_close=self.on_close)
       
       #Listening on a websocket, any way to automatically get the map.png?
       self.guid_list = []
       self.team_drivers = []
       self.driver_names = []

    # Put handeling stuff here
    def on_error(self, ws, error):
        print("Error occurred:", error)

    def on_close(self, ws):
        print("WebSocket connection closed")

    def on_open(self, ws):
        print("WebSocket connection opened")

    
    def on_message(self, ws, message):
        # Convert message string to a dictionary using JSON
        try:
            data = json.loads(message)
            #print("Parsed data:", data)
            if data["EventType"] == 200:
                self.create_car_list(data["Message"])
        except json.JSONDecodeError:
            print("Received non-JSON message:", message)

    def create_car_list(self, data):
        for driver in data["ConnectedDrivers"]["Drivers"]:
            self.guid_list.append(driver)
        for guid in self.guid_list:
            if "-YORK" in data["ConnectedDrivers"]["Drivers"][guid]["CarInfo"]["DriverName"] and data["ConnectedDrivers"]["Drivers"][guid]["CarInfo"] not in self.team_drivers:
                self.team_drivers.append(data["ConnectedDrivers"]["Drivers"][guid]["CarInfo"])
                self.driver_names.append(data["ConnectedDrivers"]["Drivers"][guid]["CarInfo"]["DriverName"])
                print(self.team_drivers[0]["CarID"], self.team_drivers[0]["DriverName"])
                #print(self.driver_names)

                
reader = WebsocketReader()
reader.ws.on_open = reader.on_open(reader.ws)
reader.ws.run_forever()