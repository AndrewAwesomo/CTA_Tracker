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

class Clock:
    def __init__(self, master):
        self.master = master
        self.update_frame()

    def update_frame(self):
        try:
            self.frame.destroy() # get rid of any old container frames so the new labels don't stack on each other
        except:
            pass
        self.frame = Frame(self.master)  # create new parent frame to jam each train direction frame into
        self.frame.pack()
        t = datetime.now().time()
        time = t.strftime('%I:%M:%S.%f%p')[:-9] + ' ' + t.strftime('%I:%M:%S.%f%p')[-2:]
        self.clockLabel = Label(self.frame, text=time)
        self.clockLabel.config(font=('Courier', 50))
        self.clockLabel.grid(row=0, sticky=N+W+S+E)
        self.master.after(1000, self.update_frame)


class Train:
    def __init__(self, master, TRAIN_API_KEY, TRAIN_STATION, UPDATE_TIME):
        self.TRAIN_API_KEY = TRAIN_API_KEY
        self.TRAIN_STATION = TRAIN_STATION
        self.UPDATE_TIME = UPDATE_TIME
        self.heading = Label(master, text='Train Tracker', bg='green', fg='white')
        self.heading.config(font=('Courier', 20))
        self.heading.pack(fill=X)
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
        build_labels(self.frame, trains)
        self.master.after(self.UPDATE_TIME * 1000, self.update_frame)


class Bus:
    def __init__(self, master, BUS_API_KEY, BUS_STATION, UPDATE_TIME):
        self.BUS_API_KEY = BUS_API_KEY
        self.BUS_STATION = BUS_STATION
        self.UPDATE_TIME = UPDATE_TIME
        self.heading = Label(master, text='Bus Tracker', bg='green', fg='white')
        self.heading.config(font=('Courier', 20))
        self.heading.pack(fill=X)
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
        build_labels(self.frame, buses)
        self.master.after(self.UPDATE_TIME * 1000, self.update_frame)



def build_labels(master, transits):
    # get direction data from feed
    if 'destSt' in transits[0]:  # for trains
        directions = set(transit['stpId'] for transit in transits)
    if 'des' in transits[0]:  # for buses
        directions = set(transit['stpid'] for transit in transits)
    directions = list(directions)
    directions.sort()

    # filter directions
    filteredTrans = []
    for direction in directions:
        if 'destSt' in transits[0]:  # for trains
            filteredTrans.append([transit for transit in transits if transit['stpId'] == direction])
        if 'des' in transits[0]:  # for buses
            filteredTrans.append([transit for transit in transits if transit['stpid'] == direction])

    for i, direction in enumerate(filteredTrans):
        childFrame = Frame(master, pady=5, bd=2, relief=GROOVE)  # create new frame for each direction/stop
        childFrame.grid_columnconfigure(0, weight=1)
        childFrame.grid(row=i, sticky=NW + NE)
        for j, trans in enumerate(direction):
            # for trains
            if 'destSt' in trans:
                eta = datetime.strptime(trans['arrT'].replace('T', " "), '%Y-%m-%d %H:%M:%S') - datetime.now()
                eta = formatEta(eta)
                destination = trans['destNm']
                station = trans['staNm']
                route = trans['rt']
                label = Label(childFrame,
                                   text='{} Line from {} toward {} -> {}'.format(route, station, destination, eta),
                                   bg='blue', fg='white', anchor=W)

            # for buses
            if 'des' in trans:
                eta = datetime.strptime(trans['prdtm'], '%Y%m%d %H:%M') - datetime.now()
                eta = formatEta(eta)
                destination = trans['des']
                direction = trans['rtdir']
                station = trans['stpnm']
                route = trans['rt']
                label = Label(childFrame,
                                   text='Route {} from {} {} to {} -> {}'.format(route, station, direction, destination,
                                                                                 eta), bg='blue', fg='white', anchor=W)

            label.config(font=('Courier', 26))
            label.grid(row=j, sticky=W + E)
    return master


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

clockFrame = Frame(root, padx=5, bd=2, relief=GROOVE)
clockFrame.grid(row=0, column=1, sticky=W)
Clock(clockFrame)

busFrame = Frame(root, padx=5, bd=2, relief=GROOVE)
busFrame.grid(row=1, column=0, sticky=NW, columnspan=2)
Bus(busFrame, BUS_API_KEY, BUS_STATION, UPDATE_TIME)
root.mainloop()