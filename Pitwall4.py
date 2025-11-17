import pygame, requests, connecttest2, config_test

pygame.init()

screen = pygame.display.set_mode((1500, 800))
global clock
clock = pygame.time.Clock()
pygame.display.set_caption("Car Obama")

text_font = pygame.font.SysFont("Roboto Normal", 40)



class new_driver:
    def __init__(self, x, y, z, ID, name, tyre, split, pos, pit, no_pits, long_pit, drs, blue, best_lap, last_lap, york_driver):
        self.x = x
        self.y = y
        self.z = z
        self.ID = ID
        self.name = str(name)
        self.tyre = tyre
        self.split = split
        self.pos = pos
        self.pit = pit
        self.no_pits = no_pits
        self.long_pit = long_pit
        self.drs = drs
        self.blue = blue
        self.best_lap = best_lap
        self.last_lap = last_lap
        self.is_york_driver = york_driver


    def return_ID(self):
        return str(self.ID)
    
    def return_name(self):
        return self.name[0:8]
    
    def return_tyre(self):
        return self.tyre
    
    def return_split(self):
        return str(self.split)
    
    def return_pos(self):
        return str(self.pos)
    
    def return_pit(self):
        return self.pit

    def return_pit_no(self):
        pit_no = str(self.no_pits)
        return pit_no
    

    def sort_time(self, time):
        lap_seconds = float(time) / 1000000000
        lap_mins = int(lap_seconds // 60)
        lap_seconds = lap_seconds - (lap_mins * 60)
        lap_seconds = round(lap_seconds, 3)
        if lap_seconds < 10:
            last_lap = str(lap_mins)+ ":0"+ str(lap_seconds)
        else:
            last_lap = str(lap_mins)+ ":"+ str(lap_seconds)
        return last_lap
    

    def return_last_lap(self):
        last_lap = self.sort_time(self.last_lap)
        return last_lap
    
    def return_best_lap(self):
        best_lap = self.sort_time(self.best_lap)
        return best_lap



def load_map(server, map_layout):
    #Fetching trackmap
    map_link = ""
    if server == "wss://yorkfs.emperorservers.com/api/race-control":
        map_link = "https://yorkfs.emperorservers.com/content/tracks/"+ map_layout[0]+ "/"+ map_layout[1]+ "/map.png"
    else:
        map_link = "https://fs-server-1.emperorservers.com/content/tracks/"+ map_layout[0]+ "/"+ map_layout[1]+ "/map.png"

    track = requests.get(map_link).content
    image = open("track_map.png", "wb")
    image.write(track)
    image.close()

    global track_map
    track_map = pygame.image.load("track_map.png").convert_alpha()
    
    #Need to scale the image so if width height greater than 300 - 400 scale so it is
    scale = 1
    while track_map.get_height() > 300 or track_map.get_width() > 400:
        scale -= 0.02
        track_map = pygame.transform.scale_by(track_map, scale)

    #print(track_map.get_height(), track_map.get_width())



def live_timing(driver_list):
    import pandas as pd
    pygame.draw.rect(screen, (31, 42, 68), (10, 10, 400, 300), 2)
    data = []
    index_list = []
    if len(driver_list) != 0:
        for i in range(len(driver_list)):
            temp_list = []

            index_list.append(driver_list[i].return_pos())

            temp_list.append(driver_list[i].return_name())
            temp_list.append(driver_list[i].return_tyre())
            temp_list.append(driver_list[i].return_last_lap())
        
            data.append(temp_list)

        df = str(pd.DataFrame(data, index= index_list, columns = ["Driver", "Tyre", "Last Lap"]))
    
        lines = df.split("\n")

        offset = 0

        for k in range(len(lines)):
            #print(k)
            if k == 0:
                #Add the spaces to the text here for only the column headings - lines[k][i] = lines[k][i] + "  "
                example_text = text_font.render(lines[k],False, (255, 255, 255))
                screen.blit(example_text, (510, 40 + offset))
            else:    
                example_text = text_font.render(lines[k],False, (255, 255, 255))
                screen.blit(example_text, (500, 40 + offset))
            offset += 50

def sort_drivers(driver_list):
    for u in range(len(driver_list)):
        print(driver_list[u].return_pos())
    
    if len(driver_list) > 1:
        if int(driver_list[0].return_pos()) != 1:
            driver_data = driver_list[0]
            driver_list.remove(driver_list[0])
            placed = False
            i = 0
            while not placed:
                if i >= len(driver_list):
                    placed = True
                elif int(driver_data.return_pos()) < int(driver_list[i].return_pos()):
                    driver_list.insert(i, driver_data)
                    placed = True
                else:
                    i += 1
    
    return driver_list
    


def redraw(server, driver):
    screen.blit(track_map,(10,10))
    york_data = connecttest2.fetch_driver_data(server, driver)
    
    #live_timing(york_data)
    driver_list = []
    #Could be issue with using york_data[0], might need to do york_data[len(york_data)-1]
    if len(york_data) != 0:
        York_driver = new_driver(york_data[0]["LastPos"]["X"], york_data[0]["LastPos"]["Y"], york_data[0]["LastPos"]["Z"], york_data[0]["CarInfo"]["CarID"], 
                                york_data[0]["CarInfo"]["DriverName"], york_data[0]["CarInfo"]["Tyres"], york_data[0]["Split"], 
                                york_data[0]["Position"], york_data[0]["IsInPits"], york_data[0]["NumPits"], york_data[0]["NumLongPits"],
                                york_data[0]["DRSActive"], york_data[0]["BlueFlag"], york_data[0]["Cars"][york_data[0]["CarInfo"]["CarModel"]]["BestLap"],
                                york_data[0]["Cars"][york_data[0]["CarInfo"]["CarModel"]]["LastLap"], True)
        driver_list.append(York_driver)
    york_data = connecttest2.fetch_other_data(server, driver)
    if len(york_data) != 0:
        for o in range(len(york_data)):
            New_driver = new_driver(york_data[o]["LastPos"]["X"], york_data[o]["LastPos"]["Y"], york_data[o]["LastPos"]["Z"], york_data[o]["CarInfo"]["CarID"], 
                                york_data[o]["CarInfo"]["DriverName"], york_data[o]["CarInfo"]["Tyres"], york_data[o]["Split"], 
                                york_data[o]["Position"], york_data[o]["IsInPits"], york_data[o]["NumPits"], york_data[o]["NumLongPits"],
                                york_data[o]["DRSActive"], york_data[o]["BlueFlag"], york_data[o]["Cars"][york_data[o]["CarInfo"]["CarModel"]]["BestLap"],
                                york_data[o]["Cars"][york_data[o]["CarInfo"]["CarModel"]]["LastLap"], False)
            driver_list.append(New_driver)
    sorted_drivers = sort_drivers(driver_list)
    live_timing(sorted_drivers)




def draw_layout():
    screen.fill((31, 42, 68)) #Background
    pygame.draw.rect(screen, (0, 0, 0), (10, 10, 400, 300), 2) #Leaderboard box
    pygame.draw.rect(screen, (0, 0, 0), (500, 10, 950, 300), 2) #Map box

def fetch_info():
    import config_test
    config_data = config_test.read_config()
    return_list = []
    return_list.append(config_data["Driver No"])
    if config_data["Server"] == "Server 1":
        return_list.append("wss://fs-server-1.emperorservers.com/api/race-control")
    elif config_data["Server"] == "Server 2":
        return_list.append("wss://fs-server-2.emperorservers.com/api/race-control")
    elif config_data["Server"] == "Server 3":
        return_list.append("wss://fs-server-3.emperorservers.com/api/race-control")
    elif config_data["Server"] == "Server YFS":
        return_list.append("wss://yorkfs.emperorservers.com/api/race-control")
    
    return return_list
        
def run():
    config_info = fetch_info()
    driver = config_info[0]
    server = config_info[1]
    running = True
    #Need to fetch the track and layout from message 200 and then import into load_map()
    map_layout = connecttest2.fetch_map_data(server, driver)
    load_map(server, map_layout)
    
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        clock.tick(15)
        draw_layout()
        redraw(server, driver)
        pygame.display.update()

run()