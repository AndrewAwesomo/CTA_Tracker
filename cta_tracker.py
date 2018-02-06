import requests
from tkinter import *
from datetime import datetime
import ast

# read in API keys as dictionary
with open('api_keys.txt', 'r') as f:
    keyDict = ast.literal_eval(f.read())

TRAIN_API_KEY = keyDict['Train']
BUS_API_KEY = keyDict['Bus']
TRAIN_STATION = '41410'  # Chicago (Blue)
BUS_STATION = '563,615,5500,5525'
UPDATE_TIME = 15  # set number of seconds between updates


class Train:
    def __init__(self, master, TRAIN_API_KEY, TRAIN_STATION, UPDATE_TIME):
        self.TRAIN_API_KEY = TRAIN_API_KEY
        self.TRAIN_STATION = TRAIN_STATION
        self.UPDATE_TIME = UPDATE_TIME
        self.heading = Label(master, text='Train Tracker')
        self.heading.pack()
        self.master = master
        self.update_frame()

    def update_frame(self):
        try:
            self.frame.destroy() # get rid of any old container frames so the new labels don't stack on each other
        except:
            pass
        self.frame = Frame(self.master)  # create new parent frame to jam each train direction frame into
        self.frame.pack()
        response = requests.get('http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key=' + self.TRAIN_API_KEY
                                + '&mapid=' + self.TRAIN_STATION + '&outputType=JSON')
        trains = response.json()['ctatt']['eta'] # get rid of the wrappers

        # get direction data from feed
        directions = set(train['stpId'] for train in trains)
        directions = list(directions)
        directions.sort()

        # filter train directions
        filteredTrains = []
        for direction in directions:
            filteredTrains.append([train for train in trains if train['stpId'] == direction])

        for i, direction in enumerate(filteredTrains):
            self.childFrame = Frame(self.frame, pady=5, bd=2, relief=GROOVE) # create new frame for each direction
            self.childFrame.grid_columnconfigure(0, weight=1)
            self.childFrame.grid(row=i, sticky=NW + NE)
            for j, train in enumerate(direction): # create a new label for each train in a single direction
                eta = datetime.strptime(train['arrT'].replace('T', " "), '%Y-%m-%d %H:%M:%S') - datetime.now()
                eta = formatEta(eta)
                destination = train['destNm']
                station = train['staNm']
                route = train['rt']
                self.label = Label(self.childFrame,
                                   text='{} Line from {} toward {} -> {}'.format(route, station, destination, eta),
                                   bg='blue', fg='white', anchor=W)
                self.label.grid(row=j, sticky=W + E)
        self.master.after(self.UPDATE_TIME * 1000, self.update_frame)


class Bus:
    def __init__(self, master, BUS_API_KEY, BUS_STATION, UPDATE_TIME):
        self.BUS_API_KEY = BUS_API_KEY
        self.BUS_STATION = BUS_STATION
        self.UPDATE_TIME = UPDATE_TIME
        self.heading = Label(master, text='Bus Tracker')
        self.heading.pack()
        self.master = master
        self.update_frame()

    def update_frame(self):
        try:
            self.frame.destroy()
        except:
            pass
        self.frame = Frame(self.master)
        self.frame.pack()
        response = requests.get('http://www.ctabustracker.com/bustime/api/v2/getpredictions?key='
                                + self.BUS_API_KEY + '&stpid=' + self.BUS_STATION + '&format=json')
        buses = response.json()['bustime-response']['prd']

        # get direction data from feed
        directions = set(bus['stpid'] for bus in buses)
        directions = list(directions)
        directions.sort()

        # filter bus directions
        filteredBuses = []
        for direction in directions:
            filteredBuses.append([bus for bus in buses if bus['stpid'] == direction])

        for i, direction in enumerate(filteredBuses):
            self.childFrame = Frame(self.frame, pady=5, bd=2, relief=GROOVE)  # create new frame for each direction/stop
            self.childFrame.grid_columnconfigure(0, weight=1)
            self.childFrame.grid(row=i, sticky=NW + NE)
            for j, bus in enumerate(direction):
                eta = datetime.strptime(bus['prdtm'], '%Y%m%d %H:%M') - datetime.now()
                eta = formatEta(eta)
                destination = bus['des']
                direction = bus['rtdir']
                station = bus['stpnm']
                route = bus['rt']
                self.label = Label(self.childFrame,
                                   text='Route {} from {} {} to {} -> {}'.format(route, station, direction, destination,
                                                                                 eta),
                                   bg='blue', fg='white', anchor=W)
                self.label.grid(row=j, sticky=W + E)
        self.master.after(self.UPDATE_TIME * 1000, self.update_frame)


def formatEta(eta):
    minutes = (eta.seconds // 60) % 60
    seconds = str(eta.seconds % 60).zfill(2)
    if minutes > 55 or minutes < 1:
        return 'Due'
    else:
        return '{}:{}'.format(minutes, seconds)


root = Tk()
root.winfo_toplevel().title('CTA Tracker: Updates Every {} seconds'.format(UPDATE_TIME))
trainFrame = Frame(root, padx=5, bd=2, relief=GROOVE)
trainFrame.grid(row=0, column=0, sticky=NW)
Train(trainFrame, TRAIN_API_KEY, TRAIN_STATION, UPDATE_TIME)

busFrame = Frame(root, padx=5, bd=2, relief=GROOVE)
busFrame.grid(row=0, column=1, sticky=NW)
Bus(busFrame, BUS_API_KEY, BUS_STATION, UPDATE_TIME)
root.mainloop()